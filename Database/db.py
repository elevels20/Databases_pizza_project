from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
#from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

from Database.Models.base import Base

# Replace with your own credentials
DATABASE_URL = 'mysql+pymysql://root:19042004@localhost/PizzaServiceDB'
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
print("SessionLocal created")
# call session.commit() to save changes to the database manually

# Function to initialize the database (creates tables)
def init_db():
    Base.metadata.create_all(bind=engine)

# Session = sessionmaker(bind=engine)
# session = Session()

# session.close()