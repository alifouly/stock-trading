from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from database import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True)
    price = Column(Numeric)
    availability = Column(Numeric)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    funds = Column(Numeric)

class UserStock(Base):
    __tablename__ = "user_stocks"

    user_id = Column(Integer, primary_key=True)
    stock_id = Column(String, primary_key=True)
    total = Column(Integer)