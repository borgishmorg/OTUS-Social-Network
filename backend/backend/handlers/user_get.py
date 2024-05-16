from datetime import date
from uuid import UUID

from pydantic import BaseModel

from backend.dependencies.database import ReplicaConnection
from backend.exceptions import UserNotFoundException


class UserGetResponse(BaseModel):
    id: UUID
    first_name: str
    second_name: str
    birthdate: date
    biography: str
    city: str


SQL_QUERY = '''
SELECT
    id,
    first_name,
    second_name,
    birthdate,
    biography,
    city
FROM users
WHERE id = %(id)s
LIMIT 1;
'''


async def user_get(
    user_id: UUID,
    db: ReplicaConnection,
) -> UserGetResponse:
    cur = await db.execute(SQL_QUERY, {'id': user_id})
    if not (row := await cur.fetchone()):
        raise UserNotFoundException
    return UserGetResponse(**row)
