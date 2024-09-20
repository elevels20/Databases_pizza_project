from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists
from database import engine
from tables.dessert import Dessert

Session = sessionmaker(bind=engine)
session = Session()


desserts = [
    Dessert(name='Ice Cream', price=4.0),
    Dessert(name='Cheesecake', price=5.5),
    Dessert(name='Brownie', price=3.0),
    Dessert(name='Apple Pie', price=4.5),
    Dessert(name='Tiramisu', price=6.0)
]


for dessert in desserts:

    dessert_exists = session.query(exists().where(Dessert.name == dessert.name)).scalar()

    if not dessert_exists:
        session.add(dessert)

    else:
        print(f"{dessert.name} already exists in the database.")


session.commit()


session.close()

print("Dessert addition process completed!")

