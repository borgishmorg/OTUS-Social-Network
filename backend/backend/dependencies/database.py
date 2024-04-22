from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator

import psycopg
import psycopg_pool
from fastapi import Depends
from psycopg.rows import DictRow, dict_row

from backend.settings import settings

_pool: psycopg_pool.AsyncConnectionPool


@asynccontextmanager
async def pool_lifespan():
    global _pool
    async with psycopg_pool.AsyncConnectionPool(
        settings.DB_CONN,
        kwargs={
            'row_factory': dict_row,
        },
        max_size=settings.DB_POOL_MAX_SIZE,
    ) as pool:
        _pool = pool
        yield


async def connection() -> AsyncGenerator[psycopg.AsyncConnection[DictRow], None]:
    global _pool
    async with _pool.connection() as aconn:
        try:
            yield aconn
        except Exception:
            await aconn.rollback()
            raise
        else:
            await aconn.commit()


Connection = Annotated[psycopg.AsyncConnection[DictRow], Depends(connection)]
