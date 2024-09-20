from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class DeliveryPerson(Base):
    __tablename__ = 'delivery_person'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    postal_code_area_id = Column(Integer, ForeignKey('postal_code_area.id'), nullable=False)
    availability = Column(Boolean, nullable=False)
    current_order_id = Column(Integer, ForeignKey('orders.id'), nullable=True)
    unavailable_until = Column(DateTime, nullable=True)

    current_order = relationship("Order", back_populates="delivery_person")
    postal_code_area = relationship("PostalCodeArea", back_populates="delivery_person")
