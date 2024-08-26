from contextlib import asynccontextmanager

from aio_pika import ExchangeType, IncomingMessage, Message

from backend.dependencies.cache import _cache
from backend.dependencies.database import replica_connection
from backend.dependencies.rabbitmq import channel
from backend.services.feed import PostFeedItem, PostFeedsService
from backend.settings import settings


@asynccontextmanager
async def feeds_update_background_task():
    async def on_message(message: IncomingMessage):
        async with message.process():
            parsed = PostFeedItem.model_validate_json(message.body)

            cur = await db.execute(
                GET_SUBSCRIBERS_IDS_QUERY,
                params={
                    'user_id': parsed.author_user_id,
                },
            )

            for row in await cur.fetchall():
                # добавляем пост в закэшированную ленту
                await post_feeds_service.add_post_to_feed(
                    user_id=row['user_id'],
                    feed_item=parsed,
                )
                # отправляем пост в очередь для вэбсокета
                await outgoing_exchange.publish(
                    Message(message.body),
                    routing_key=settings.FEEDS_QUEUE_TEMPLATE.format_map(row),
                )

    async with (
        asynccontextmanager(replica_connection)() as db,
        asynccontextmanager(channel)() as chan,
    ):
        await chan.set_qos(1)

        incoming_queue = await chan.declare_queue(
            settings.POSTS_QUEUE,
            durable=True,
        )
        outgoing_exchange = await chan.declare_exchange(
            settings.FEEDS_EXCHANGE,
            ExchangeType.DIRECT,
        )
        post_feeds_service = PostFeedsService(
            db=db,
            cache=_cache,
        )

        await incoming_queue.consume(on_message)
        yield


GET_SUBSCRIBERS_IDS_QUERY = '''
SELECT
    user_id
FROM user_friends
WHERE friend_id = %(user_id)s;
'''
