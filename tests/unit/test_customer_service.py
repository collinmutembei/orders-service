import pytest
from unittest.mock import Mock
from src.services.customer_service import CustomerService
from src.schemas.customer import CustomerCreate, CustomerDetails
from src.ports.repository import CustomerRepository


@pytest.fixture
def mock_customer_repo():
    return Mock(spec=CustomerRepository)


@pytest.fixture
def customer_service(mock_customer_repo):
    return CustomerService(repository=mock_customer_repo)


def test_create_customer(customer_service, mock_customer_repo):
    customer_create = CustomerCreate(
        name="Test Customer", phone="254712345678", code="12345678"
    )

    mock_customer_repo.create_customer = Mock(
        return_value=CustomerDetails(
            id=1,
            name=customer_create.name,
            phone=customer_create.phone,
            code=customer_create.code,
        )
    )

    result = customer_service.create_customer(customer_create)

    mock_customer_repo.create_customer.assert_called_once_with(customer_create)
    assert isinstance(result, CustomerDetails)
    assert result.id == 1
    assert result.name == customer_create.name
    assert result.phone == customer_create.phone
    assert result.code == customer_create.code


def test_get_customer_by_id(customer_service, mock_customer_repo):
    customer_id = 1
    mock_customer = CustomerDetails(
        id=customer_id,
        name="Test Customer",
        phone="254712345678",
        code="12345678",
    )
    mock_customer_repo.get_customer_by_id = Mock(return_value=mock_customer)

    result = customer_service.get_customer_by_id(customer_id)

    mock_customer_repo.get_customer_by_id.assert_called_once_with(customer_id)
    assert result == mock_customer


def test_get_customer_by_phone(customer_service, mock_customer_repo):
    phone = "254712345678"
    mock_customer = CustomerDetails(
        id=1,
        name="Test Customer",
        phone=phone,
        code="12345678",
    )
    mock_customer_repo.get_customer_by_phone = Mock(return_value=mock_customer)

    result = customer_service.get_customer_by_phone(phone)

    mock_customer_repo.get_customer_by_phone.assert_called_once_with(phone)
    assert result == mock_customer


def test_get_customer_by_code(customer_service, mock_customer_repo):
    code = "12345678"
    mock_customer = CustomerDetails(
        id=1,
        name="Test Customer",
        phone="254712345678",
        code=code,
    )
    mock_customer_repo.get_customer_by_code = Mock(return_value=mock_customer)

    result = customer_service.get_customer_by_code(code)

    mock_customer_repo.get_customer_by_code.assert_called_once_with(code)
    assert result == mock_customer


def test_get_customer_not_found(customer_service, mock_customer_repo):
    customer_id = 999
    mock_customer_repo.get_customer_by_id = Mock(return_value=None)

    result = customer_service.get_customer_by_id(customer_id)

    mock_customer_repo.get_customer_by_id.assert_called_once_with(customer_id)
    assert result is None
