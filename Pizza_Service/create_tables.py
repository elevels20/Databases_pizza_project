from database import engine
from tables.base import Base

Base.metadata.create_all(engine)
