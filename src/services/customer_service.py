from src.schemas.customer import CustomerCreate
from src.ports.repository import CustomerRepository


class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    def get_customer_by_id(self, customer_id: int):
        return self.repository.get_customer_by_id(customer_id)

    def get_customer_by_phone(self, phone: str):
        return self.repository.get_customer_by_phone(phone)

    def create_customer(self, customer_data: CustomerCreate):
        return self.repository.create_customer(customer_data)

    def get_customer_by_code(self, code: str):
        return self.repository.get_customer_by_code(code)

    def update_customer_phone(self, customer_id: int, phone: str):
        return self.repository.update_customer_phone(customer_id, phone)
