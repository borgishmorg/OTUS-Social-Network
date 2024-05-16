from contextlib import asynccontextmanager
from typing import Annotated, AsyncGenerator

import psycopg
import psycopg_pool
from fastapi import Depends
from psycopg.rows import DictRow, dict_row

from backend.settings import settings

_primary_pool: psycopg_pool.AsyncConnectionPool
_replica_pool: psycopg_pool.AsyncConnectionPool


@asynccontextmanager
async def pools_lifespan():
    global _primary_pool
    global _replica_pool
    async with (
        psycopg_pool.AsyncConnectionPool(
            settings.DB_CONN_PRIMARY,
            kwargs={
                'row_factory': dict_row,
            },
            max_size=settings.DB_POOL_MAX_SIZE,
        ) as primary_pool,
        psycopg_pool.AsyncConnectionPool(
            settings.DB_CONN_REPLICA,
            kwargs={
                'row_factory': dict_row,
            },
            max_size=settings.DB_POOL_MAX_SIZE,
        ) as replica_pool,
    ):
        _primary_pool = primary_pool
        _replica_pool = replica_pool
        yield


async def connection() -> AsyncGenerator[psycopg.AsyncConnection[DictRow], None]:
    global _primary_pool
    async with _primary_pool.connection() as aconn:
        try:
            yield aconn
        except Exception:
            await aconn.rollback()
            raise
        else:
            await aconn.commit()


async def replica_connection() -> AsyncGenerator[psycopg.AsyncConnection[DictRow], None]:
    global _replica_pool
    async with _replica_pool.connection() as aconn:
        try:
            yield aconn
        except Exception:
            await aconn.rollback()
            raise
        else:
            await aconn.commit()


Connection = Annotated[psycopg.AsyncConnection[DictRow], Depends(connection)]
ReplicaConnection = Annotated[psycopg.AsyncConnection[DictRow], Depends(replica_connection)]
