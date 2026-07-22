from fastapi import APIRouter, HTTPException
from models import Transaction, TransactionResponse
from database import cursor, conn
from services import transaction_service

transaction_router = APIRouter()

@transaction_router.post("/" , status_code= 201)
def post_transaction(transaction : Transaction):
    transaction_service.add_transaction(transaction)
    return {"message": "Transaction added"}


@transaction_router.get("/", response_model=list[TransactionResponse])
def get_all_transactions():
    transactions = transaction_service.show_transactions()
    return transactions


@transaction_router.put("/{id}")
def put_transaction_by_id(transaction: Transaction, id: int):
    transaction_service.update_transaction(transaction, id)
    return {"message": "Transaction edited successfully."}


@transaction_router.delete("/{id}")
def delete_transactions(id: int):
    transaction_service.delete_transaction(id)
    return {"message": "Transaction deleted successfully"}


@transaction_router.get("/{id}", response_model=TransactionResponse)
def get_transaction_by_id(id: int):
    transaction = transaction_service.show_transactions_by_id(id)    
    return transaction


