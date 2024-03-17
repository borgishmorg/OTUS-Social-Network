from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt
from pydantic import BaseModel

from backend.settings import settings


class LoginRequest(BaseModel):
    id: UUID
    password: str


class LoginResponse(BaseModel):
    token: str


async def login(request: LoginRequest) -> LoginResponse:
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

