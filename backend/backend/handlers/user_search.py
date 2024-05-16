from backend.dependencies.database import ReplicaConnection
from backend.handlers.user_get import UserGetResponse

SQL_QUERY = '''
select
    id,
    first_name,
    second_name,
    birthdate,
    biography,
    city
from users
where lower(first_name) like %(first_name)s || '%%'
    and lower(second_name) like %(last_name)s || '%%'
order by id
limit 25;
'''


async def user_search(
    first_name: str,
    last_name: str,
    db: ReplicaConnection,
) -> list[UserGetResponse]:
    cur = await db.execute(SQL_QUERY, {'first_name': first_name.lower(), 'last_name': last_name.lower()})
    return [
        UserGetResponse(**row)
        async for row in cur
    ]
