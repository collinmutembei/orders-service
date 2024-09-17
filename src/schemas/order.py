from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class OrderBase(BaseModel):
    item: str
    amount: float


class OrderCreate(OrderBase):
    customer_id: int


class OrderDetails(OrderBase):
    id: int
    created_at: datetime
    customer_id: int

    model_config = ConfigDict(from_attributes=True)
