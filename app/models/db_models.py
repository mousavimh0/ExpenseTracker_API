from sqlalchemy import Column, Integer, String
from app.database import Base 


class TransactionDB(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    type = Column(String)
    amount = Column(Integer)
    category = Column(String)
    date = Column(String)

class UserDB(Base):
    __tablename__  = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
