from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, Request, WebSocket, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.settings import settings


# HTTPBearer не умеет работать с вэбсокетами(
class CustomHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request = None, websocket: WebSocket = None):
        return await super().__call__(request or websocket)


bearer_scheme = CustomHTTPBearer()


async def authorized(creds: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]) -> None:
    try:
        payload: dict = jwt.decode(
            jwt=creds.credentials,
            key=settings.JWT_SECRET,
            algorithms=['HS256'],
        )
        return UUID(payload['id'])
    except (
        jwt.ExpiredSignatureError,
        jwt.InvalidSignatureError,
        jwt.DecodeError,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


Authorized = Annotated[UUID, Depends(authorized)]
