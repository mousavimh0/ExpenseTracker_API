from sqlalchemy import Column, Integer, String
from app.database import Base 


class TransactionDB(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    type = Column(String)
    amount = Column(Integer)
    category = Column(String)
    date = Column(String)


