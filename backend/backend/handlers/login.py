from datetime import datetime, timedelta, timezone
from uuid import UUID

import bcrypt
import jwt
from pydantic import BaseModel

from backend.dependencies.database import Connection
from backend.exceptions import UserNotFoundException
from backend.settings import settings


class LoginRequest(BaseModel):
    id: UUID
    password: str


class LoginResponse(BaseModel):
    token: str


SQL_QUERY = '''
SELECT
    id,
    password_hash
FROM users
WHERE id = %(id)s
LIMIT 1;
'''


async def login(
    request: LoginRequest,
    db: Connection,
) -> LoginResponse:
    cur = await db.execute(
        SQL_QUERY,
        params={'id': request.id},
    )
    partial_user = await cur.fetchone()

    if not (
        partial_user
        and bcrypt.checkpw(
            request.password.encode(),
            partial_user.get('password_hash', b'')
        )
    ):
        raise UserNotFoundException

    token = jwt.encode(
        payload={
            'exp': datetime.now(timezone.utc) + timedelta(days=1),
            'id': request.id.hex,
        },
        key=settings.JWT_SECRET,
        algorithm='HS256',
    )
    return LoginResponse(
        token=token,
    )
