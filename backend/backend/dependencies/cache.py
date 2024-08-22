from typing import Annotated

from fastapi import Depends

# Здесь может быть redis или любая другая in-memory БД
# Но для учебных целей используется словарь
_cache: dict = dict()


Cache = Annotated[dict, Depends(lambda: _cache)]
