import pytest
from unittest.mock import patch, Mock
from fastapi import HTTPException
from jose import jwt
from src.adapters.auth import get_auth, get_current_user
from src.config import settings
from src.models.customer import Customer
from src.schemas.customer import CustomerCreate


pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_oauth2_scheme():
    return Mock()


@pytest.fixture
def mock_customer_service():
    return Mock()


@pytest.fixture
def valid_token():
    return "valid.jwt.token"


@pytest.fixture
def decoded_token():
    return {
        "sub": "user123",
        "name": "John Doe",
        "phone_number": "1234567890",
        "aud": "account",
    }


@patch("src.adapters.auth.jwt.decode")
async def test_get_auth_valid_token(mock_jwt_decode, valid_token, decoded_token):
    mock_jwt_decode.return_value = decoded_token

    result = await get_auth(valid_token)

    assert result == decoded_token
    mock_jwt_decode.assert_called_once_with(
        valid_token,
        key=f"-----BEGIN PUBLIC KEY-----\n{settings.KEYCLOAK_PUBLIC_KEY}\n-----END PUBLIC KEY-----",
        algorithms=["RS256"],
        audience="account",
        options={
            "verify_signature": True,
            "verify_aud": True,
            "exp": True,
        },
    )


@patch("src.adapters.auth.jwt.decode")
async def test_get_auth_invalid_token(mock_jwt_decode, valid_token):
    mock_jwt_decode.side_effect = jwt.JWTError("Invalid token")

    with pytest.raises(HTTPException) as exc_info:
        await get_auth(valid_token)

    assert exc_info.value.status_code == 401
    assert "Invalid authentication credentials" in str(exc_info.value.detail)


@patch("src.adapters.auth.jwt.decode")
async def test_get_auth_unexpected_error(mock_jwt_decode, valid_token):
    mock_jwt_decode.side_effect = Exception("Unexpected error")

    with pytest.raises(HTTPException) as exc_info:
        await get_auth(valid_token)

    assert exc_info.value.status_code == 401
    assert "Invalid authentication credentials" in str(exc_info.value.detail)


async def test_get_current_user_existing_customer(mock_customer_service, decoded_token):
    existing_customer = Customer(
        id=1, code="user123", name="John Doe", phone="1234567890"
    )
    mock_customer_service.get_customer_by_code.return_value = existing_customer

    result = await get_current_user(decoded_token, mock_customer_service)

    assert result == existing_customer
    mock_customer_service.get_customer_by_code.assert_called_once_with("user123")
    mock_customer_service.create_customer.assert_not_called()


async def test_get_current_user_new_customer(mock_customer_service, decoded_token):
    mock_customer_service.get_customer_by_code.return_value = None
    new_customer = Customer(id=1, code="user123", name="John Doe", phone="1234567890")
    mock_customer_service.create_customer.return_value = new_customer

    result = await get_current_user(decoded_token, mock_customer_service)

    assert result == new_customer
    mock_customer_service.get_customer_by_code.assert_called_once_with("user123")
    mock_customer_service.create_customer.assert_called_once_with(
        CustomerCreate(code="user123", name="John Doe", phone="1234567890")
    )
