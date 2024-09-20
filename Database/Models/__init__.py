#from sqlalchemy.ext.declarative import declarative_base

#from ..db import Base
from .customer import Customer, CustomerAccount, DiscountCode
from .orders import Orders, OrderPizza, OrderDrink, OrderDessert
from .delivery import DeliveryPerson, PostalCodeArea
from .menu import Pizza, Drink, Dessert
from .ingredients import Ingredient, PizzaIngredient

#Base = declarative_base()