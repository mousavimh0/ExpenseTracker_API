from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.transaction import Transaction, TransactionResponse
from app.repositories import transaction_repository, user_repository
from app.models.db_models import TransactionDB, UserDB


def show_transactions(db: Session, user_id) -> list[TransactionDB]:
    transactions = transaction_repository.select_all(db, user_id)

    return transactions


def add_transaction(transaction: Transaction, db: Session, user_id):
    user = user_repository.get_user_by_id(db, transaction.user_id)
    if not user:
        raise HTTPException(404, "user not found")
    transaction_repository.insert_transaction(transaction, db, user_id)


def update_transaction(transaction: Transaction, id: int, db: Session, user_id):

    transaction_repository.update_transaction(transaction, id, db, user_id)


def delete_transaction(id: int, db: Session, user_id):
    transaction_repository.delete_transaction(id, db, user_id)


def show_transactions_by_id(id: int, db: Session, user_id) -> dict:
    transaction = transaction_repository.select_transaction_by_id(id, db, user_id)

    return transaction
