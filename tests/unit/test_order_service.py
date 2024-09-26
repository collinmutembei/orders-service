import pytest
from datetime import datetime
from unittest.mock import Mock
from src.services.order_service import OrderService
from src.schemas.order import OrderCreate, OrderDetails
from src.ports.repository import SQLAlchemyOrderRepository


@pytest.fixture
def mock_order_repo():
    return Mock(spec=SQLAlchemyOrderRepository)


@pytest.fixture
def order_service(mock_order_repo):
    return OrderService(repository=mock_order_repo)


def test_create_order(order_service, mock_order_repo):
    order_create = OrderCreate(item="Test Item", amount=19.99, customer_id=1)
    created_at = datetime.now()

    mock_order_repo.create_order = Mock(
        return_value=OrderDetails(
            id=1,
            customer_id=1,
            item=order_create.item,
            amount=order_create.amount,
            created_at=created_at,
        )
    )

    result = order_service.create_order(order_create)

    mock_order_repo.create_order.assert_called_once_with(order_create)
    assert isinstance(result, OrderDetails)
    assert result.id == 1
    assert result.customer_id == 1
    assert result.item == order_create.item
    assert result.amount == order_create.amount


def test_get_order_by_id(order_service, mock_order_repo):
    order_id = 1
    customer_id = 1
    mock_order = OrderDetails(
        id=order_id,
        customer_id=customer_id,
        item="Test Item",
        amount=11.99,
        created_at=datetime.now(),
    )
    mock_order_repo.get_order_by_id = Mock(return_value=mock_order)

    result = order_service.get_order_by_id(order_id, customer_id)

    mock_order_repo.get_order_by_id.assert_called_once_with(order_id, customer_id)
    assert result == mock_order


def test_get_order_not_found(order_service, mock_order_repo):
    order_id = 999
    customer_id = 1
    mock_order_repo.get_order_by_id = Mock(return_value=None)

    result = order_service.get_order_by_id(order_id, customer_id)

    mock_order_repo.get_order_by_id.assert_called_once_with(order_id, customer_id)
    assert result is None


def test_get_orders(order_service, mock_order_repo):
    customer_id = 1
    mock_orders = [
        OrderDetails(
            id=1,
            customer_id=customer_id,
            item="Item 1",
            amount=19.99,
            created_at=datetime.now(),
        ),
        OrderDetails(
            id=2,
            customer_id=customer_id,
            item="Item 2",
            amount=9.99,
            created_at=datetime.now(),
        ),
    ]
    mock_order_repo.list_orders = Mock(return_value=mock_orders)

    result = order_service.get_orders(customer_id)

    mock_order_repo.list_orders.assert_called_once_with(customer_id)
    assert result == mock_orders
    assert len(result) == 2
    assert all(isinstance(order, OrderDetails) for order in result)


def test_get_orders_empty(order_service, mock_order_repo):
    customer_id = 1
    mock_order_repo.list_orders = Mock(return_value=[])

    result = order_service.get_orders(customer_id)

    mock_order_repo.list_orders.assert_called_once_with(customer_id)
    assert result == []


def test_create_order_with_invalid_data(order_service, mock_order_repo):
    order_create = OrderCreate(item="Invalid Item", amount=-1, customer_id=99)

    with pytest.raises(ValueError):
        order_service.create_order(order_create)

    mock_order_repo.create_order.assert_not_called()
