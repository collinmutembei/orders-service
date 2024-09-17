from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = config("DEBUG", default=False)
    DATABASE_URL: str = config("DATABASE_URL")
    AFRICASTALKING_API_KEY: str = config("AFRICASTALKING_API_KEY")
    AFRICASTALKING_USERNAME: str = config("AFRICASTALKING_USERNAME")


settings = Settings()
