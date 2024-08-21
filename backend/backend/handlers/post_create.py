from uuid import UUID

from pydantic import BaseModel

from backend.dependencies.database import Connection
from backend.dependencies.security import Authorized


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
) -> PostCreateResponse:
    cur = await db.execute(SQL_QUERY, {
        'user_id': user_id,
        'text': request.text,
    })
    return PostCreateResponse(**(await cur.fetchone()))
