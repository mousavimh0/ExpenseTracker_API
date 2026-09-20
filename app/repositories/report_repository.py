from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.db_models import TransactionDB
from fastapi import HTTPException


def sum_amount(type, db: Session, user_id: int):
    statement = select(func.sum(TransactionDB.amount)).where(
        TransactionDB.type == type, TransactionDB.user_id == user_id
    )
    result = db.execute(statement).scalar()
    if result:
        return result
    else:
        raise HTTPException(404, "Transaction not found")


def select_all(db: Session, user_id: int) -> list:

    statement = select(TransactionDB).where(TransactionDB.user_id == user_id)
    result = db.execute(statement)
    transactions = result.scalars().all()
    if transactions:
        return transactions
    else:
        raise HTTPException(404, "Transaction not found")


def select_by_column(db: Session, column, value):
    statement = select(TransactionDB).where(column == value)
    result = db.execute(statement)
    transactions = result.scalars().all()
    if transactions:
        return transactions
    else:
        raise HTTPException(404, "Transaction not found")
