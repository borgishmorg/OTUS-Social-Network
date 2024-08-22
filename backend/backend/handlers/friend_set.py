from uuid import UUID

from fastapi import Depends
from psycopg.errors import ForeignKeyViolation
from pydantic import BaseModel

from backend.dependencies.database import Connection
from backend.dependencies.security import Authorized
from backend.exceptions import UserNotFoundException
from backend.services.feed import PostFeedsService


class FriendSetResponse(BaseModel):
    description: str = 'Пользователь успешно указал своего друга'


SQL_QUERY = '''
INSERT INTO user_friends(
    user_id,
    friend_id
) VALUES (
    %(user_id)s,
    %(friend_id)s
)
ON CONFLICT DO NOTHING;
'''


async def friend_set(
    user_id: Authorized,
    friend_id: UUID,
    db: Connection,
    post_feeds_service: PostFeedsService = Depends(PostFeedsService),
) -> FriendSetResponse:
    try:
        await db.execute(SQL_QUERY, {
            'user_id': user_id,
            'friend_id': friend_id,
        })
    except ForeignKeyViolation:
        raise UserNotFoundException

    with post_feeds_service.with_db(db):
        await post_feeds_service.invalidate_single_feed(user_id=user_id)

    return FriendSetResponse()
