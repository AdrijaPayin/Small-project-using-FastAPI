from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

db_url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="Trisha@2006",
    host="localhost",
    port=5432,
    database="Products"
)

engine = create_engine(db_url)
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)