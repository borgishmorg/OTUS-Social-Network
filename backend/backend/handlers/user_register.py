from datetime import date
from uuid import UUID

import bcrypt
from pydantic import BaseModel

from backend.dependencies.database import Connection


class UserRegisterRequest(BaseModel):
    first_name: str
    second_name: str
    birthdate: date
    biography: str
    city: str
    password: str


class UserRegisterResponse(BaseModel):
    user_id: UUID


SQL_QUERY = '''
INSERT INTO users(
    first_name,
    second_name,
    birthdate,
    biography,
    city,
    password_hash
) VALUES (
    %(first_name)s,
    %(second_name)s,
    %(birthdate)s,
    %(biography)s,
    %(city)s,
    %(password_hash)s
)
RETURNING id AS user_id;
'''


async def user_register(
    request: UserRegisterRequest,
    db: Connection,
) -> UserRegisterResponse:
    params = request.model_dump(exclude=['password'])
    params['password_hash'] = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt())
    cur = await db.execute(SQL_QUERY, params)
    return UserRegisterResponse(**(await cur.fetchone()))
