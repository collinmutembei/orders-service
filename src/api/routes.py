from typing import Annotated, List
from fastapi import APIRouter, Depends
from src.schemas.customer import CustomerDetails
from src.models.customer import Customer
from src.adapters.auth import get_current_user
from src.services.customer_service import CustomerService
from src.api.deps import get_customer_service

customers_router = APIRouter()


# Customer routes
@customers_router.put(
    "/customers/",
    response_model=CustomerDetails,
    dependencies=[Depends(get_current_user)],
)
def update_customer(
    phone_number: str,
    customer: Annotated[Customer, Depends(get_current_user)],
    service: CustomerService = Depends(get_customer_service),
):
    """Set or update the authenticated customer's phone number

    Args:
        phone_number: string formatted phone number to set or update, i.e "+254711223344"

    Returns:
        The updated customer details
    """
    return service.update_customer_phone(customer.id, phone_number)
