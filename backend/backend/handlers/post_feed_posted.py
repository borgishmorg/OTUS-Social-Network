import aio_pika
from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder
from fastapi.websockets import WebSocketState

from backend.dependencies.rabbitmq import RMQChannel
from backend.dependencies.security import Authorized
from backend.services.feed import PostFeedItem
from backend.settings import settings


async def post_feed_posted(
    *,
    websocket: WebSocket,
    rmqchannel: RMQChannel,
    user_id: Authorized,
) -> None:
    async def on_message(message: aio_pika.message.IncomingMessage) -> None:
        async with message.process():
            await websocket.send_json(jsonable_encoder(PostFeedItem.model_validate_json(message.body)))

    await websocket.accept()

    incoming_exchange = await rmqchannel.declare_exchange(
        settings.FEEDS_EXCHANGE,
        aio_pika.ExchangeType.DIRECT,
    )
    incoming_queue = await rmqchannel.declare_queue(exclusive=True)
    await incoming_queue.bind(
        incoming_exchange,
        routing_key=settings.FEEDS_QUEUE_TEMPLATE.format(user_id=user_id),
    )

    await incoming_queue.consume(on_message)

    while websocket.client_state == WebSocketState.CONNECTED:
        await websocket.receive()
