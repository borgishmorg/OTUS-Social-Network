from pydantic_settings import BaseSettings

__ALL__ = 'settings',


class Settings(BaseSettings):
    JWT_SECRET: str = 'secret'

    DB_CONN_PRIMARY: str = 'host=localhost port=5432 dbname=otus-sn user=otus-sn password=otus-sn'
    DB_CONN_REPLICA: str = 'host=localhost port=5433 dbname=otus-sn user=otus-sn password=otus-sn'
    DB_POOL_MAX_SIZE: int = 100

    RABBITMQ_CONN: str = 'amqp://guest:guest@localhost/'
    POSTS_QUEUE: str = 'posts'
    FEEDS_EXCHANGE: str = 'feeds'
    FEEDS_QUEUE_TEMPLATE: str = 'feeds/{user_id}'


settings = Settings()
