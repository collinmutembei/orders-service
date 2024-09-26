from typing import Annotated, List
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from src.schemas.customer import CustomerDetails
from src.models.customer import Customer
from src.adapters.auth import get_current_user
from src.schemas.order import OrderBase, OrderCreate, OrderDetails
from src.services.customer_service import CustomerService
from src.services.order_service import OrderService
from src.api.deps import get_order_service, get_customer_service

orders_router = APIRouter()
customers_router = APIRouter()


# Orders Routes
@orders_router.get("/orders/")
def get_customer_orders(
    customer: Annotated[Customer, Depends(get_current_user)],
    service: OrderService = Depends(get_order_service),
):
    """
    Get all orders for authenticated customer. A customer can only see their own orders.

    Args:
        customer: The authenticated customer

    Returns:
        A list of orders for the customer
    """
    return service.get_orders(customer.id)


@orders_router.post("/orders/", response_model=OrderDetails)
def create_order(
    order: OrderBase,
    background_tasks: BackgroundTasks,
    customer: Annotated[Customer, Depends(get_current_user)],
    service: OrderService = Depends(get_order_service),
):
    """
    Create an order and send a notification message through SMS to the authenticated customer's phone number

    Args:
        order: The order to create

    Returns:
        The created order
    """
    customer_order = OrderCreate(
        item=order.item, amount=order.amount, customer_id=customer.id
    )
    order = service.create_order(customer_order)
    if order.customer.phone:
        background_tasks.add_task(
            service.sms_sender.send_sms,
            order.customer.phone,
            message=f"Order {order.id} created",
        )
    return order


@orders_router.get(
    "/orders/{order_id}",
    response_model=OrderDetails,
    dependencies=[Depends(get_current_user)],
)
def get_order_by_id(
    order_id: int,
    customer: Annotated[Customer, Depends(get_current_user)],
    service: OrderService = Depends(get_order_service),
):
    """
    Get an order by id for the authenticated customer

    Args:
        order_id: The id of the order to get

    Returns:
        The order with the given id
    """
    customer_id = customer.id
    order = service.get_order_by_id(order_id, customer_id)
    if not order:
        raise HTTPException(
            status_code=404,
            detail=f"Order with id {order_id} not found for customer {customer_id}",
        )
    return order


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
