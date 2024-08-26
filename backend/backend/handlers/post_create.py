from uuid import UUID

import aio_pika
from pydantic import BaseModel

from backend.dependencies.database import Connection
from backend.dependencies.rabbitmq import RMQChannel
from backend.dependencies.security import Authorized
from backend.services.feed import PostFeedItem
from backend.settings import settings


class PostCreateRequest(BaseModel):
    text: str


class PostCreateResponse(BaseModel):
    post_id: UUID


SQL_QUERY = '''
INSERT INTO posts(
    user_id,
    text
) VALUES (
    %(user_id)s,
    %(text)s
)
returning id as post_id;
'''


async def post_create(
    user_id: Authorized,
    request: PostCreateRequest,
    db: Connection,
    rmqchannel: RMQChannel,
) -> PostCreateResponse:
    cur = await db.execute(SQL_QUERY, {
        'user_id': user_id,
        'text': request.text,
    })
    response = PostCreateResponse(**(await cur.fetchone()))

    # send post to rabbitmq
    queue = await rmqchannel.declare_queue(
        settings.POSTS_QUEUE,
        durable=True,
    )
    await rmqchannel.default_exchange.publish(
        aio_pika.Message(
            PostFeedItem(
                id=response.post_id,
                text=request.text,
                author_user_id=user_id,
            ).model_dump_json().encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
        ),
        routing_key=queue.name,
    )

    return response
