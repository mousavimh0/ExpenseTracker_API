from fastapi import HTTPException
from app.schemas.models import Transaction, TransactionResponse
from app.repositories import transaction_repository
from sqlalchemy.orm import Session
from app.models.db_models import TransactionDB

def to_response(transaction: TransactionDB):
    response_items = TransactionResponse(id= transaction.id, type= transaction.type , amount= transaction.amount, category= transaction.category, date_= transaction.date)
    return response_items
    

def show_transactions(db : Session )->list:
    transactions = transaction_repository.select_all(db)
    response_list = []
    for item in transactions:
        response_list.append(
            to_response(item)
        )

    return response_list


def add_transaction(transaction: Transaction, db : Session):
    transaction_repository.insert_transaction(transaction, db)


def update_transaction(transaction : Transaction, id: int, db : Session):

    transaction_repository.update_transaction(transaction, id, db)


def delete_transaction(id: int, db : Session):
    transaction_repository.delete_transaction(id, db)


def show_transactions_by_id(id:int, db : Session)->dict:
    transaction = transaction_repository.select_transaction_by_id(id, db)
    response_items = to_response(transaction)
    return response_items

