from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
import logging
from keycloak import KeycloakOpenID
from pydantic import Json
from src.schemas.customer import CustomerCreate
from src.api.deps import get_customer_service
from src.services.customer_service import CustomerService
from src.models.customer import Customer
from src.config import settings

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.KEYCLOAK_AUTH_SERVER_URL,
    tokenUrl=settings.KEYCLOAK_TOKEN_URL,
)
keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_AUTH_SERVER_URL,
    client_id=settings.OPENID_CONNECT_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
    client_secret_key=settings.OPENID_CONNECT_CLIENT_SECRET,
    verify=True,
)


async def get_auth(token: str = Security(oauth2_scheme)) -> Json:
    try:
        public_key = f"""-----BEGIN PUBLIC KEY-----
{settings.KEYCLOAK_PUBLIC_KEY}
-----END PUBLIC KEY-----"""

        decoded_token = jwt.decode(
            token,
            key=public_key,
            algorithms=["RS256"],
            audience="account",
            options={
                "verify_signature": True,
                "verify_aud": True,
                "exp": True,
            },
        )
        return decoded_token

    except JWTError as e:
        logging.error(f"JWT decoding error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logging.error(f"Unexpected error during authentication: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(
    identity: Json = Depends(get_auth),
    customer_service: CustomerService = Depends(get_customer_service),
) -> Customer:
    customer = customer_service.get_customer_by_code(identity["sub"])
    if not customer:
        customer_data = CustomerCreate(
            code=identity.get("sub"),
            name=identity.get("name"),
            phone=identity.get("phone_number"),
        )
        customer = customer_service.create_customer(customer_data)
    return customer
