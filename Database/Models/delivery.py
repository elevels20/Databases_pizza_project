from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
#from ..db import Base
#from Database.Models import Base
from .base import Base

class DeliveryPerson(Base):
    __tablename__ = 'delivery_person'

    DeliveryPersonID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(32), nullable=False)
    PostalCodeID = Column(Integer, ForeignKey('postal_code_area.PostalCodeAreaID'), nullable=False)
    Availability = Column(Boolean, nullable=False, default=True)
    CurrentOrderID =  Column(Integer, ForeignKey('orders.OrderID'), nullable=True)
    UnavailableUntil = Column(DateTime, nullable=True, default=None)

    current_order = relationship("Orders", back_populates="delivery_person")
    postal_code_area = relationship("PostalCodeArea", back_populates="delivery_person")

class PostalCodeArea(Base):
    __tablename__ = 'postal_code_area'

    PostalCodeAreaID = Column(Integer, primary_key=True, autoincrement=True)
    PostalCode = Column(String(6), nullable=False)
    City = Column(String(32), nullable=False)
    DeliveryPersonCount = Column(Integer, nullable=False)

    delivery_person = relationship("DeliveryPerson", back_populates="postal_code_area")
