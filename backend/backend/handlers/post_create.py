from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel

from backend.dependencies.database import Connection
from backend.dependencies.security import Authorized
from backend.services.feed import PostFeedsService


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
    post_feeds_service: PostFeedsService = Depends(PostFeedsService),
) -> PostCreateResponse:
    cur = await db.execute(SQL_QUERY, {
        'user_id': user_id,
        'text': request.text,
    })
    response = PostCreateResponse(**(await cur.fetchone()))
    await post_feeds_service.add_post_to_feeds(
        user_id=user_id,
        post_id=response.post_id,
        text=request.text,
    )
    return response
