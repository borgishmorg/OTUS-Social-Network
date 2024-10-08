from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.background.feeds import feeds_update_background_task
from backend.dependencies.cache import _cache
from backend.dependencies.database import pools_lifespan, replica_connection
from backend.handlers.debug_cache import debug_cache
from backend.handlers.friend_delete import friend_delete
from backend.handlers.friend_set import friend_set
from backend.handlers.login import login
from backend.handlers.post_create import post_create
from backend.handlers.post_feed import post_feed
from backend.handlers.post_feed_posted import post_feed_posted
from backend.handlers.post_get import post_get
from backend.handlers.user_get import user_get
from backend.handlers.user_register import user_register
from backend.handlers.user_search import user_search
from backend.services.feed import PostFeedsService


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with (
        pools_lifespan(),
        asynccontextmanager(replica_connection)() as db,
        feeds_update_background_task(),
    ):
        post_feeds_service = PostFeedsService(
            db=db,
            cache=_cache,
        )
        await post_feeds_service.invalidate_all_feeds()

        yield


app = FastAPI(lifespan=lifespan)

app.add_api_route('/debug/cache', debug_cache, methods=['GET'])
app.add_api_route('/login', login, methods=['POST'])
app.add_api_route('/user/register', user_register, methods=['POST'])
app.add_api_route('/user/get/{user_id}', user_get, methods=['GET'])
app.add_api_route('/user/search', user_search, methods=['GET'])
app.add_api_route('/friend/set/{friend_id}', friend_set, methods=['PUT'])
app.add_api_route('/friend/delete/{friend_id}', friend_delete, methods=['PUT'])
app.add_api_route('/post/create', post_create, methods=['POST'])
app.add_api_route('/post/get/{post_id}', post_get, methods=['GET'])
app.add_api_route('/post/feed', post_feed, methods=['GET'])
app.add_api_websocket_route('/post/feed/posted', post_feed_posted)
