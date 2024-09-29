from src.services.customer_service import CustomerService
from src.adapters.database import get_db
from src.services.order_service import OrderService
from src.ports.repository import SQLAlchemyOrderRepository, SQLAlchemyCustomerRepository


def get_order_service():
    db = next(get_db())
    repository = SQLAlchemyOrderRepository(db)
    return OrderService(repository)


def get_customer_service():
    db = next(get_db())
    repository = SQLAlchemyCustomerRepository(db)
    return CustomerService(repository)
