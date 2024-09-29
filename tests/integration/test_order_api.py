import pytest
from unittest.mock import MagicMock, patch
from src.models.order import Order
from src.models.customer import Customer


@pytest.fixture
def valid_order_data(test_db):
    return {"item": "Test Item", "amount": 100.00, "customer_id": 1}


@pytest.fixture
def mock_sms_messager():
    sms_sender = MagicMock()
    sms_sender.send_sms.return_value = {"status": "success"}
    return sms_sender


def test_create_order_success(
    authenticated_client,
    mock_order_service,
    valid_order_data,
    mock_sms_messager,
    test_db,
):
    mock_order = Order(id=1, **valid_order_data)
    mock_order_service.create_order.return_value = mock_order

    with patch("src.api.routes.create_order", return_value=mock_order_service):
        response = authenticated_client.post(
            "/orders/",
            json=valid_order_data,
        )

    assert response.status_code == 200
    assert response.json()["created_at"] is not None
    assert response.json()["id"] is not None
    assert response.json()["item"] == "Test Item"
    assert response.json()["amount"] == 100.00
    assert response.json()["customer_id"] == 1


def test_create_order_invalid_data(authenticated_client):
    invalid_data = {"item": "Test Item", "customer_id": 1}
    response = authenticated_client.post("/orders/", json=invalid_data)
    assert response.status_code == 422


def test_create_unauthenticated(client, valid_order_data):
    response = client.post("/orders/", json=valid_order_data)
    assert response.status_code == 401


def test_get_orders_success(authenticated_client, mock_order_service):
    mock_orders = [
        Order(id=1, customer_id=1, item="Test Item", amount=100.00),
        Order(id=2, customer_id=1, item="Test Item 2", amount=200.00),
    ]
    mock_order_service.get_orders.return_value = mock_orders

    response = authenticated_client.get("/orders/")
    assert response.status_code == 200


def test_get_orders_by_id(
    authenticated_client, mock_order_service, valid_order_data, test_db
):
    mock_order = Order(id=1, **valid_order_data)
    mock_order_service.get_order_by_id.return_value = mock_order

    response = authenticated_client.get("/orders/1")
    assert response.status_code == 404


def test_get_orders_by_id_not_found(authenticated_client, mock_order_service):
    mock_order_service.get_order_by_id.return_value = None

    response = authenticated_client.get("/orders/99")
    assert response.status_code == 404
