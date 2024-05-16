from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    JWT_SECRET: str = 'secret'

    DB_CONN_PRIMARY: str = 'host=localhost port=5432 dbname=otus-sn user=otus-sn password=otus-sn'
    DB_CONN_REPLICA: str = 'host=localhost port=5433 dbname=otus-sn user=otus-sn password=otus-sn'
    DB_POOL_MAX_SIZE: int = 100


settings = Settings()
