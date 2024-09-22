from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import pymysql
from Database.Models.base import Base

# Replace with your own credentials
DATABASE_URL = 'mysql+pymysql://root:19042004@localhost/PizzaServiceDB'

# Connect to MySQL without specifying a database (to create one if needed)
# Again replace with your own credentials
engine_without_db = create_engine('mysql+pymysql://root:19042004@localhost')

# Try to create the database
try:
    with engine_without_db.connect() as conn:
        conn.execute(text("CREATE DATABASE IF NOT EXISTS PizzaServiceDB"))
        print("Database 'PizzaServiceDB' created (or it already exists)")
except OperationalError as e:
    print(f"Error creating database: {e}")


engine = create_engine(DATABASE_URL)
#Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, bind=engine)
print("SessionLocal created")
# call session.commit() to save changes to the database manually

# Function to initialize the database (creates tables)
def init_db():
    Base.metadata.create_all(bind=engine)

# Session = sessionmaker(bind=engine)
# session = Session()

# session.close()