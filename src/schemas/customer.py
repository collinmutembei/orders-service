from typing import Optional
from pydantic import BaseModel, ConfigDict


class CustomerBase(BaseModel):
    name: str
    code: str
    phone: str


class CustomerCreate(CustomerBase):
    phone: Optional[str]


class CustomerDetails(CustomerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
