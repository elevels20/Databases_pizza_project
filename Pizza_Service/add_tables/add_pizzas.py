from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists
from database import engine
from tables.pizza import Pizza

Session = sessionmaker(bind=engine)
session = Session()


pizzas = [
    Pizza(name='margarita', price=0.0, diet=''),
    Pizza(name='pepperoni', price=0.0, diet=''),
    Pizza(name='hawaii', price=0.0, diet=''),
    Pizza(name='four_cheese', price=0.0, diet=''),
    Pizza(name='bbq_chicken', price=0.0, diet=''),
    Pizza(name='veggie', price=0.0, diet=''),
    Pizza(name='meat_lovers', price=0.0, diet=''),
    Pizza(name='buffalo_chicken', price=0.0, diet=''),
    Pizza(name='spinach_feta', price=0.0, diet=''),
    Pizza(name='truffle_mushroom', price=0.0, diet='')
]


for pizza in pizzas:
    pizza_exists = session.query(exists().where(Pizza.name == pizza.name)).scalar()
    if not pizza_exists:
        session.add(pizza)

    else:
        print(f"{pizza.name} already exists in the database.")

session.commit()
session.close()

print("Pizza addition process completed!")
