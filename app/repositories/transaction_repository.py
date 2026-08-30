from app.schemas.transaction import Transaction
from app.models.db_models import TransactionDB
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import select
from app.core import exeptions


def select_all(db: Session, user_id, skip, limit) -> list:

    statement = (
        select(TransactionDB)
        .where(TransactionDB.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    result = db.execute(statement)
    transactions = result.scalars().all()
    return transactions


def select_transaction_by_id(id, db: Session, user_id):

    statement = select(TransactionDB).where(
        TransactionDB.id == id, TransactionDB.user_id == user_id
    )
    transaction = db.execute(statement).scalar_one_or_none()
    if transaction:
        return transaction
    else:
        raise exeptions.NotFoundException("not found", "transaction not found.")


def insert_transaction(transaction: Transaction, db: Session, user_id):

    new_transaction = TransactionDB(
        type=transaction.type,
        amount=transaction.amount,
        category=transaction.category,
        date_=transaction.date_,
        user_id=user_id,
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction


def update_transaction(transaction: Transaction, id, db: Session, user_id):
    statement = select(TransactionDB).where(
        TransactionDB.id == id, TransactionDB.user_id == user_id
    )
    result = db.execute(statement)
    updating_transaction = result.scalar_one_or_none()

    if updating_transaction:
        updating_transaction.type = transaction.type
        updating_transaction.amount = transaction.amount
        updating_transaction.category = transaction.category
        updating_transaction.date_ = transaction.date_
        updating_transaction.user_id = user_id

        db.commit()
        db.refresh(updating_transaction)
        return updating_transaction
    else:
        raise exeptions.NotFoundException("not found", "transaction not found.")


def delete_transaction(id, db: Session, user_id):
    statement = select(TransactionDB).where(
        TransactionDB.id == id, TransactionDB.user_id == user_id
    )
    transaction = db.execute(statement).scalar_one_or_none()

    if transaction:
        db.delete(transaction)
        db.commit()
    else:
        raise exeptions.NotFoundException("not found", "transaction not found.")
