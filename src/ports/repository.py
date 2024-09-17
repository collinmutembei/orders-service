from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.customer import Customer
from src.schemas.customer import CustomerCreate
from src.models.order import Order
from src.schemas.order import OrderCreate


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
