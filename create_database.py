import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Database.db import SessionLocal, init_db
import subprocess

# Initialize the database (create tables if not exists)
init_db()

# adding pizzas, drinks, desserts and ingredients to db
subprocess.run(["python3", "Data/add_menu_data.py"])

# adding ingredients, prices and diets to pizzas in db
subprocess.run(["python3", "Data/add_pizza_ingredients.py"])

