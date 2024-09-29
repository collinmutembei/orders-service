from faker import Faker
from src.ports.repository import SQLAlchemyCustomerRepository, SQLAlchemyOrderRepository
from src.adapters.database import get_db

faker = Faker()


def test_create_customer(test_customer_data):
    db = next(get_db())
    repository = SQLAlchemyCustomerRepository(db)

    for test_customer in test_customer_data:
        customer = repository.create_customer(test_customer)
        assert customer.id is not None
        assert customer.name == test_customer.name
        assert customer.phone == test_customer.phone
        assert customer.code == test_customer.code


def test_get_customer_by_id(test_customer_data):
    db = next(get_db())
    repository = SQLAlchemyCustomerRepository(db)

    for test_customer in test_customer_data:
        customer_in_db = repository.create_customer(test_customer)
        customer = repository.get_customer_by_id(customer_in_db.id)
        assert customer is not None
        assert customer.id == customer_in_db.id
        assert customer.name == test_customer.name
        assert customer.phone == test_customer.phone


def test_get_customer_by_id_not_found():
    db = next(get_db())
    repository = SQLAlchemyCustomerRepository(db)

    customer = repository.get_customer_by_id(9999)
    assert customer is None


def test_get_customer_by_phone(test_customer_data):
    db = next(get_db())
    repository = SQLAlchemyCustomerRepository(db)

    for test_customer in test_customer_data:
        customer_in_db = repository.create_customer(test_customer)
        customer = repository.get_customer_by_phone(customer_in_db.phone)
        assert customer is not None
        assert customer.name == test_customer.name
        assert customer.phone == test_customer.phone


def test_customer_by_code(test_customer_data):
    db = next(get_db())
    repository = SQLAlchemyCustomerRepository(db)

    for test_customer in test_customer_data:
        customer_in_db = repository.create_customer(test_customer)
        customer = repository.get_customer_by_code(customer_in_db.code)
        assert customer is not None
        assert customer.code == test_customer.code
        assert customer.name == test_customer.name
        assert customer.phone == test_customer.phone


def test_update_customer_phone(test_customer_data):
    db = next(get_db())
    repository = SQLAlchemyCustomerRepository(db)
    phone_number = faker.basic_phone_number()
    existing_customer = repository.create_customer(test_customer_data[0])

    updated_customer = repository.update_customer_phone(
        existing_customer.id, phone_number
    )

    assert updated_customer.phone == phone_number


def test_create_order(test_order_data):
    db = next(get_db())
    repository = SQLAlchemyOrderRepository(db)

    for test_order in test_order_data:
        order = repository.create_order(test_order)
        assert order.id is not None
        assert order.item == test_order.item
        assert order.amount == test_order.amount
        assert order.customer_id == test_order.customer_id


def test_get_order_by_id(test_order_data):
    db = next(get_db())
    repository = SQLAlchemyOrderRepository(db)

    for test_order in test_order_data:
        order_in_db = repository.create_order(test_order)
        order = repository.get_order_by_id(order_in_db.id, order_in_db.customer_id)
        assert order is not None
        assert order.id == order_in_db.id
