import asyncio
from contextlib import asynccontextmanager

import tqdm
from mimesis import Address, Person, Text
from mimesis.locales import Locale

from backend.dependencies.database import connection, pools_lifespan

BATCH_COUNT = 100
BATCH_SIZE = 10_000
PERSON = Person(Locale.RU)
ADDRESS = Address(Locale.RU)
TEXT = Text(Locale.RU)
PASSWORD_HASH_HEX = (
    '2432622431322437694c6f526b6c56'
    '79515356437369334e6247664a654c'
    '4f6c79566a474541492f4f685a6456'
    '5377436a316d54774e46534a737475'
)  # password
QUERY = '''
INSERT INTO users(
    first_name,
    second_name,
    birthdate,
    biography,
    city,
    password_hash
) VALUES (
    %(first_name)s,
    %(second_name)s,
    %(birthdate)s,
    %(biography)s,
    %(city)s,
    %(password_hash)s
);
'''


async def main():
    async with (
        pools_lifespan(),
        asynccontextmanager(connection)() as conn,
        conn.cursor() as cur
    ):
        for _ in tqdm.trange(BATCH_COUNT, desc='Batches (10k rows each)'):
            await cur.executemany(
                query=QUERY,
                params_seq=[
                    {
                        'first_name': PERSON.first_name(),
                        'second_name': PERSON.last_name(),
                        'birthdate': PERSON.birthdate(),
                        'biography': TEXT.text(),
                        'city': ADDRESS.city(),
                        'password_hash': bytes.fromhex(PASSWORD_HASH_HEX),
                    }
                    for _ in range(BATCH_SIZE)
                ]
            )


if __name__ == '__main__':
    asyncio.run(main())
