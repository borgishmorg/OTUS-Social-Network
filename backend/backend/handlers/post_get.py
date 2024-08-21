from uuid import UUID

from pydantic import BaseModel

from backend.dependencies.database import Connection
from backend.exceptions import PostNotFoundException


class PostGetResponse(BaseModel):
    text: str


SQL_QUERY = '''
SELECT text
FROM posts
WHERE id = %(post_id)s
;
'''


async def post_get(
    post_id: UUID,
    db: Connection,
) -> PostGetResponse:
    cur = await db.execute(SQL_QUERY, {
        'post_id': post_id,
    })
    if not (row := await cur.fetchone()):
        raise PostNotFoundException
    return PostGetResponse(**row)
