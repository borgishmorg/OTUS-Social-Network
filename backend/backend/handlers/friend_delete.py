from uuid import UUID

from fastapi import Depends
from pydantic import BaseModel

from backend.dependencies.database import Connection
from backend.dependencies.security import Authorized
from backend.services.feed import PostFeedsService


class FriendDeleteResponse(BaseModel):
    description: str = 'Пользователь успешно удалил из друзей пользователя'


SQL_QUERY = '''
DELETE FROM user_friends
WHERE
    user_id = %(user_id)s
    AND friend_id = %(friend_id)s
;
'''


async def friend_delete(
    user_id: Authorized,
    friend_id: UUID,
    db: Connection,
    post_feeds_service: PostFeedsService = Depends(PostFeedsService),
) -> FriendDeleteResponse:
    await db.execute(SQL_QUERY, {
        'user_id': user_id,
        'friend_id': friend_id,
    })

    with post_feeds_service.with_db(db):
        await post_feeds_service.invalidate_single_feed(user_id=user_id)

    return FriendDeleteResponse()
