from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.engine import URL
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

url = "sqlite:///database.db"
engine = create_engine(url)
connection = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
