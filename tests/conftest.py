import random
from faker import Faker
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.services.customer_service import CustomerService
from src.services.order_service import OrderService
from src.ports.repository import (
    SQLAlchemyCustomerRepository,
    SQLAlchemyOrderRepository,
)
from src.schemas.order import OrderCreate
from src.schemas.customer import CustomerCreate

from src.models.customer import Customer
from src.adapters.auth import get_current_user, get_auth
from src.adapters.database import Base, get_db
from src.main import api
from unittest.mock import MagicMock

faker = Faker()

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


api.dependency_overrides[get_db] = override_get_db


def authencation_data():
    return {
        "sub": "user123",
        "name": "John Doe",
        "phone": "1234567890",
    }


def authenticated_user():
    return Customer(id=1, code="user123", name="John Doe", phone="1234567890")


@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(api)
    Base.metadata.drop_all(bind=engine)
    api.dependency_overrides.clear()


@pytest.fixture
def authenticated_client():
    Base.metadata.create_all(bind=engine)
    api.dependency_overrides[get_auth] = authencation_data
    api.dependency_overrides[get_current_user] = authenticated_user
    yield TestClient(api)
    Base.metadata.drop_all(bind=engine)
    api.dependency_overrides.clear()


@pytest.fixture
def test_customer_data():
    customer_data = []
    for _ in range(3):
        name = faker.name()
        code = "".join([str(random.randint(0, 9)) for _ in range(9)])
        phone = faker.basic_phone_number()
        customer_data.append(CustomerCreate(name=name, code=code, phone=phone))
    return customer_data


@pytest.fixture
def test_order_data(test_customer_data):
    order_data = []
    for _ in range(3):
        item = faker.name()
        amount = faker.random_int(min=100, max=1000)
        customer_id = faker.random_int(min=1, max=len(test_customer_data))
        order_data.append(
            OrderCreate(item=item, amount=amount, customer_id=customer_id)
        )
    return order_data


@pytest.fixture
def mock_order_service():
    return MagicMock()
