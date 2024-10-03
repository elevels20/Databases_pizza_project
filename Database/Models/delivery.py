from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class DeliveryPerson(Base):
    __tablename__ = 'delivery_persons'

    delivery_person_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(32), nullable=False)
    last_name = Column(String(32), nullable=False)
    postal_code_area_id = Column(Integer, ForeignKey('postal_code_areas.postal_code_area_id'), nullable=False)
    availability = Column(Boolean, nullable=False, default=True)
    current_order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=True)
    unavailable_until = Column(DateTime, nullable=True, default=None)

    orders = relationship("Order", back_populates="delivery_person", foreign_keys="[Order.delivery_person_id]")
    postal_code_area = relationship("PostalCodeArea", back_populates="delivery_person")

class PostalCodeArea(Base):
    __tablename__ = 'postal_code_areas'

    postal_code_area_id = Column(Integer, primary_key=True, autoincrement=True)
    postal_code = Column(String(5), nullable=False)
    city = Column(String(32), nullable=False)
    delivery_person_count = Column(Integer, nullable=False)

    delivery_person = relationship("DeliveryPerson", back_populates="postal_code_area")
