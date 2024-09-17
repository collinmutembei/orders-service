from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.adapters.database import Base
from datetime import datetime, UTC


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, index=True)
    amount = Column(Float)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    customer_id = Column(Integer, ForeignKey("customers.id"))

    customer = relationship("Customer", back_populates="orders")
