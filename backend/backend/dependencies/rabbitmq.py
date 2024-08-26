from typing import Annotated, AsyncGenerator

from aio_pika import connect
from aio_pika.abc import AbstractChannel
from fastapi import Depends

from backend.settings import settings


async def channel() -> AsyncGenerator[AbstractChannel, None]:
    async with await connect(settings.RABBITMQ_CONN) as connection:
        yield await connection.channel()


RMQChannel = Annotated[AbstractChannel, Depends(channel)]
