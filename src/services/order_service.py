from src.schemas.order import OrderCreate
from src.ports.repository import OrderRepository
from src.adapters.messager import SMSMessager


class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository
        self.sms_sender = SMSMessager()

    def create_order(self, order_data: OrderCreate):
        if order_data.amount <= 0:
            raise ValueError("Amount must be greater than 0")
        order = self.repository.create_order(order_data)
        return order

    def get_order_by_id(self, order_id, customer_id):
        order = self.repository.get_order_by_id(order_id, customer_id)
        return order

    def get_orders(self, customer_id):
        orders = self.repository.list_orders(customer_id)
        return orders
