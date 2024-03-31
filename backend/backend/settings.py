from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    JWT_SECRET: str = 'secret'

    DB_CONN: str = 'host=localhost port=5432 dbname=otus-sn user=otus-sn password=otus-sn'


settings = Settings()
