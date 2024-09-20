from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists
from database import engine
from tables.drink import Drink

Session = sessionmaker(bind=engine)
session = Session()


drinks = [
    Drink(name='Coca Cola', price=2.5),
    Drink(name='Sprite', price=2.5),
    Drink(name='Fanta', price=2.5),
    Drink(name='Water', price=1.5),
    Drink(name='Orange Juice', price=3.0)
]


for drink in drinks:
    drink_exists = session.query(exists().where(Drink.name == drink.name)).scalar()
    if not drink_exists:
        session.add(drink)

    else:
        print(f"{drink.name} already exists in the database.")

session.commit()
session.close()

print("Drink addition process completed!")
