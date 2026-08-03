from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship


class TransactionDB(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    type = Column(String)
    amount = Column(Integer)
    category = Column(String)
    date_ = Column(String)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    user = relationship("UserDB", back_populates="transactions")


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    transactions = relationship(
        "TransactionDB", back_populates="user", cascade="all, delete-orphan"
    )
    role = Column(String, default="user")
