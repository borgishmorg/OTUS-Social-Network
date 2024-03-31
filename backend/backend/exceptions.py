from typing import ClassVar

from fastapi import status
from fastapi.exceptions import HTTPException


class BaseNotFoundException(HTTPException):
    DETAILS: ClassVar[str]

    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=self.DETAILS,
        )


class UserNotFoundException(BaseNotFoundException):
    DETAILS = 'USER_NOT_FOUND'
