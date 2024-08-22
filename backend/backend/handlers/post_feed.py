from fastapi import Depends

from backend.dependencies.security import Authorized
from backend.services.feed import PostFeedItem, PostFeedsService


async def post_feed(
    *,
    user_id: Authorized,
    offset: int = 0,
    limit: int = 10,
    post_feeds_service: PostFeedsService = Depends(PostFeedsService),
) -> list[PostFeedItem]:
    return await post_feeds_service.get_feed(
        user_id=user_id,
        offset=offset,
        limit=limit,
    )
