from datetime import date
from uuid import UUID, uuid4

from pydantic import BaseModel


class UserRegisterRequest(BaseModel):
    first_name: str
    second_name: str
    birthdate: date
    biography: str
    city: str
    password: str


class UserRegisterResponse(BaseModel):
    user_id: UUID


async def user_register(request: UserRegisterRequest) -> UserRegisterResponse:
    return UserRegisterResponse(
        user_id=uuid4(),
    )

