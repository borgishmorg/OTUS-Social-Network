from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.settings import settings

bearer_scheme = HTTPBearer()


async def authorized(creds: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]) -> None:
    try:
        jwt.decode(
            jwt=creds.credentials,
            key=settings.JWT_SECRET,
            algorithms=['HS256'],
        )
    except (
        jwt.ExpiredSignatureError,
        jwt.InvalidSignatureError,
        jwt.DecodeError,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


Authorized = Annotated[None, Depends(authorized)]
