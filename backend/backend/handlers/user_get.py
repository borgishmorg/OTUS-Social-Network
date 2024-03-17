from datetime import date
from uuid import UUID, uuid4

from pydantic import BaseModel

from backend.dependencies.security import Authorized


class UserGetResponse(BaseModel):
    id: UUID
    first_name: str
    second_name: str
    birthdate: date
    biography: str
    city: str


async def user_get(
    user_id: UUID,
    _: Authorized,
) -> UserGetResponse:
    return UserGetResponse(
        id=uuid4(),
        first_name='first_name',
        second_name='second_name',
        birthdate=date.today(),
        biography='biography',
        city='city',
    )
