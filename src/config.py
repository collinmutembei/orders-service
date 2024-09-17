from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = config("DEBUG", default=False)
    DATABASE_URL: str = config("DATABASE_URL")


settings = Settings()
