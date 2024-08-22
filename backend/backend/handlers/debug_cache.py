from fastapi.encoders import jsonable_encoder

from backend.dependencies.cache import Cache


async def debug_cache(
    cache: Cache,
) -> dict:
    return jsonable_encoder(cache)
