from contextlib import contextmanager
from itertools import groupby
from uuid import UUID

from pydantic import BaseModel

from backend.dependencies.cache import Cache
from backend.dependencies.database import Connection, ReplicaConnection


class PostFeedItem(BaseModel):
    id: UUID
    text: str
    author_user_id: UUID


class PostFeedsService:
    MAX_CACHED_POSTS_IN_FEED = 1000

    def __init__(
        self,
        db: ReplicaConnection,
        cache: Cache
    ) -> None:
        self._db = db
        self._cache: dict[UUID, list[PostFeedItem]] = cache

    @contextmanager
    def with_db(self, db: Connection | ReplicaConnection):
        prev_db, self._db = self._db, db
        yield
        self._db = prev_db

    async def get_feed(
        self,
        user_id: UUID,
        offset: int,
        limit: int,
    ) -> list[PostFeedItem]:
        return self._cache.get(user_id, [])[offset:offset + limit]

    async def add_post_to_feed(
        self,
        user_id: UUID,
        feed_item: PostFeedItem,
    ) -> None:
        self._cache[user_id] = [feed_item] + self._cache.get(user_id, [])[:self.MAX_CACHED_POSTS_IN_FEED - 1]

    async def invalidate_single_feed(self, user_id: UUID) -> None:
        cur = await self._db.execute(
            GET_SINGLE_FEED_QUERY,
            params={
                'user_id': user_id,
                'limit': self.MAX_CACHED_POSTS_IN_FEED,
                'offset': 0,
            },
        )
        self._cache[user_id] = [PostFeedItem(**row) for row in await cur.fetchall()]

    async def invalidate_all_feeds(self) -> None:
        cur = await self._db.execute(
            GET_ALL_FEEDS_QUERY,
            params={
                'max_feed_size': self.MAX_CACHED_POSTS_IN_FEED,
            },
        )
        for user_id, posts_data in groupby(
            await cur.fetchall(),
            lambda row: row.pop('user_id'),
        ):
            self._cache[user_id] = [PostFeedItem(**post_data) for post_data in posts_data]

    async def _get_subscribers_ids(self, user_id: UUID) -> list[UUID]:
        'Returns users which have user with user_id equal to `user_id` as friend'
        cur = await self._db.execute(
            GET_SUBSCRIBERS_IDS_QUERY,
            params={
                'user_id': user_id,
            },
        )
        return [row['user_id'] for row in await cur.fetchall()]


GET_SINGLE_FEED_QUERY = '''
select
    p.id as id,
    p.text as text,
    p.user_id as author_user_id
from
    posts p
    inner join user_friends uf on p.user_id = uf.friend_id
where
    uf.user_id = %(user_id)s
order by
    p.created desc
limit %(limit)s
offset %(offset)s
;
'''

GET_SUBSCRIBERS_IDS_QUERY = '''
SELECT
    user_id
FROM user_friends
WHERE friend_id = %(user_id)s;
'''

GET_ALL_FEEDS_QUERY = '''
select
    user_id,
    author_user_id,
    id,
    text
from (
    select
        uf.user_id as user_id,
        uf.friend_id as author_user_id,
        p.id as id,
        p.text as text,
        row_number() over (partition by uf.user_id order by created desc) as index_in_feed
    from
        user_friends uf
        inner join posts p on uf.friend_id = p.user_id
    order by
        uf.user_id,
        p.created desc
) s
where index_in_feed <= %(max_feed_size)s
order by user_id, index_in_feed
'''
