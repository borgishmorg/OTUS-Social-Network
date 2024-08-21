from uuid import UUID

from pydantic import BaseModel

from backend.dependencies.database import Connection
from backend.dependencies.security import Authorized


class PostFeedItem(BaseModel):
    id: UUID
    text: str
    author_user_id: UUID


SQL_QUERY = '''
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


async def post_feed(
    *,
    user_id: Authorized,
    offset: int = 0,
    limit: int = 10,
    db: Connection,
) -> list[PostFeedItem]:
    cur = await db.execute(SQL_QUERY, {
        'user_id': user_id,
        'limit': limit,
        'offset': offset,
    })
    return [
        PostFeedItem(**row)
        for row in await cur.fetchall()
    ]
