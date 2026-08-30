from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.transaction import Transaction, TransactionResponse
from app.repositories import transaction_repository, user_repository
from app.models.db_models import TransactionDB, UserDB
from app.core import exeptions


def show_transactions(db: Session, user_id, skip, limit) -> list[TransactionDB]:
    transactions = transaction_repository.select_all(db, user_id, skip, limit)

    return transactions


def add_transaction(transaction: Transaction, db: Session, user_id):
    user = user_repository.get_user_by_id(db, user_id)
    if not user:
        raise exeptions.NotFoundException("not found", "user not found")
    new_transaction = transaction_repository.insert_transaction(
        transaction, db, user_id
    )
    return new_transaction


def update_transaction(transaction: Transaction, id: int, db: Session, user_id):

    updating_transaction = transaction_repository.update_transaction(
        transaction, id, db, user_id
    )
    return updating_transaction


def delete_transaction(id: int, db: Session, user_id):
    transaction_repository.delete_transaction(id, db, user_id)


def show_transactions_by_id(id: int, db: Session, user_id) -> dict:
    transaction = transaction_repository.select_transaction_by_id(id, db, user_id)

    return transaction
