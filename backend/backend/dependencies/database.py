from typing import Annotated, AsyncGenerator

import psycopg
from fastapi import Depends
from psycopg.rows import DictRow, dict_row

from backend.settings import settings


async def connection() -> AsyncGenerator[psycopg.AsyncConnection[DictRow], None]:
    aconn = await psycopg.AsyncConnection.connect(
        settings.DB_CONN,
        row_factory=dict_row,
    )
    async with aconn:
        try:
            yield aconn
        except Exception:
            await aconn.rollback()
            raise
        else:
            await aconn.commit()


Connection = Annotated[psycopg.AsyncConnection[DictRow], Depends(connection)]
