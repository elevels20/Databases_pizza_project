from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class DiscountCode(Base):
    __tablename__ = 'discount_code'
    id = Column(Integer, primary_key=True)
    code = Column(String(16), nullable=False)
    discount_percentage = Column(Float, nullable=False)
    used = Column(Boolean, nullable=False)


    customer_accounts = relationship("CustomerAccount", back_populates="discount_code")
