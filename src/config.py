from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = config("DEBUG", default=False)
    DATABASE_URL: str = config("DATABASE_URL")
    KEYCLOAK_AUTH_SERVER_URL: str = config(
        "KEYCLOAK_AUTH_SERVER_URL",
        default="http://localhost:8080/realms/sso/protocol/openid-connect/auth",
    )
    KEYCLOAK_TOKEN_URL: str = config(
        "KEYCLOAK_TOKEN_URL",
        default="http://localhost:8080/realms/sso/protocol/openid-connect/token",
    )
    KEYCLOAK_REALM: str = config("KEYCLOAK_REALM", default="sso")
    KEYCLOAK_PUBLIC_KEY: str = config("KEYCLOAK_PUBLIC_KEY")
    OPENID_CONNECT_CLIENT_ID: str = config(
        "OPENID_CONNECT_CLIENT_ID", default="orders-service"
    )
    OPENID_CONNECT_CLIENT_SECRET: str = config("OPENID_CONNECT_CLIENT_SECRET")
    AFRICASTALKING_API_KEY: str = config("AFRICASTALKING_API_KEY")
    AFRICASTALKING_USERNAME: str = config("AFRICASTALKING_USERNAME")


settings = Settings()
