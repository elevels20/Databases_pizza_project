from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class PostalCodeArea(Base):
    __tablename__ = 'postal_code_area'
    id = Column(Integer, primary_key=True)
    postal_code = Column(String(6), nullable=False)
    city = Column(String(32), nullable=False)
    delivery_person_count = Column(Integer, nullable=False)

    delivery_person = relationship("DeliveryPerson", back_populates="postal_code_area")
