from uuid import UUID

from pydantic import BaseModel

from backend.dependencies.database import Connection
from backend.dependencies.security import Authorized


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
) -> FriendDeleteResponse:
    await db.execute(SQL_QUERY, {
        'user_id': user_id,
        'friend_id': friend_id,
    })
    return FriendDeleteResponse()
