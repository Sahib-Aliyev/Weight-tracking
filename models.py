from sqlalchemy import Column, Integer, String, FLOAT, DATE
from db import Base, engine


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    height = Column(FLOAT)


class WheightEntries(Base):
    __tablename__ = "weight_entries"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    weight = Column(FLOAT)
    date = Column(DATE)


Base.metadata.create_all(bind=engine)
