from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.customer import Customer
from src.schemas.customer import CustomerCreate
from src.models.order import Order
from src.schemas.order import OrderCreate
from sqlalchemy.orm.exc import NoResultFound


class OrderRepository(ABC):
    @abstractmethod
    def create_order(self, order_data: OrderCreate) -> Order:
        """Create a new order and return the created order object"""
        pass

    @abstractmethod
    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        """Retrieve an order by its ID"""
        pass

    @abstractmethod
    def list_orders(self) -> List[Order]:
        """Retrieve all orders"""
        pass


class CustomerRepository(ABC):
    @abstractmethod
    def create_customer(self, customer_data: CustomerCreate) -> Customer:
        """Create a new customer and return the created customer object"""
        pass

    @abstractmethod
    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        """Retrieve a customer by their ID"""
        pass

    @abstractmethod
    def get_customer_by_phone(self, phone: str) -> Optional[Customer]:
        """Retrieve a customer by their phone number"""
        pass

    @abstractmethod
    def get_customer_by_code(self, code: str) -> Optional[Customer]:
        """Retrieve a customer by their code"""
        pass

    @abstractmethod
    def update_customer_phone(self, customer_id: int, phone: str) -> Customer:
        """Updates customer's phone number"""
        pass


class SQLAlchemyCustomerRepository(CustomerRepository):
    def __init__(self, db_session):
        self.db_session = db_session

    def create_customer(self, customer_data: CustomerCreate) -> Customer:
        """Create a new customer and return the created customer object"""
        customer = Customer(**customer_data.model_dump())
        self.db_session.add(customer)
        self.db_session.commit()
        self.db_session.refresh(customer)
        return customer

    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        """Retrieve a customer by their ID"""
        return (
            self.db_session.query(Customer).filter(Customer.id == customer_id).first()
        )

    def get_customer_by_phone(self, phone: str) -> Optional[Customer]:
        """Retrieve a customer by their phone number"""
        return self.db_session.query(Customer).filter(Customer.phone == phone).first()

    def get_customer_by_code(self, code: str) -> Optional[Customer]:
        """Retrieve a customer by their code"""
        return self.db_session.query(Customer).filter(Customer.code == code).first()

    def update_customer_phone(self, customer_id: int, phone: str) -> Customer:
        """Updates customer's phone number"""
        customer = (
            self.db_session.query(Customer).filter(Customer.id == customer_id).first()
        )
        if not customer:
            raise ValueError(f"Customer with id {customer_id} does not exist")

        customer.phone = phone
        self.db_session.commit()
        self.db_session.refresh(customer)
        return customer


class SQLAlchemyOrderRepository(OrderRepository):
    def __init__(self, db_session):
        self.db_session = db_session

    def create_order(self, order_data: OrderCreate) -> Order:
        """Create a new order and return the created order object"""

        order = Order(**order_data.model_dump())
        self.db_session.add(order)
        self.db_session.commit()
        self.db_session.refresh(order)
        return order

    def get_order_by_id(self, order_id: int, customer_id: int) -> Optional[Order]:
        """Retrieve an order by its ID for given customer"""
        return (
            self.db_session.query(Order)
            .filter(Order.id == order_id)
            .filter(Order.customer_id == customer_id)
            .first()
        )

    def list_orders(self, customer_id: int) -> List[Order]:
        """Retrieve all orders"""
        return (
            self.db_session.query(Order).filter(Order.customer_id == customer_id).all()
        )
