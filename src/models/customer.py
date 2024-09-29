from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.adapters.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    code = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)

    orders = relationship("Order", back_populates="customer")
