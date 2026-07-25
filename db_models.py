from sqlalchemy import Column, Integer, String
from database import Base 
from database import engine

class TransactionDB(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    type = Column(String)
    amount = Column(Integer)
    category = Column(String)
    date = Column(String)


