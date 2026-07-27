from fastapi import APIRouter, Depends
from app.schemas.transaction import Transaction, TransactionResponse
from app.services import transaction_service
from app.database import get_db
from sqlalchemy.orm import Session

transaction_router = APIRouter()

@transaction_router.post("/" , status_code= 201)
def post_transaction(transaction : Transaction, db: Session = Depends(get_db)):
    transaction_service.add_transaction(transaction, db)
    return {"message": "Transaction added"}


@transaction_router.get("/", response_model=list[TransactionResponse])
def get_all_transactions(db: Session = Depends(get_db)):
    transactions = transaction_service.show_transactions(db)
    return transactions


@transaction_router.put("/{id}")
def put_transaction_by_id(transaction: Transaction, id: int, db: Session = Depends(get_db)):
    transaction_service.update_transaction(transaction, id, db)
    return {"message": "Transaction edited successfully."}


@transaction_router.delete("/{id}")
def delete_transactions(id: int, db: Session = Depends(get_db)):
    transaction_service.delete_transaction(id, db)
    return {"message": "Transaction deleted successfully"}


@transaction_router.get("/{id}", response_model=TransactionResponse)
def get_transaction_by_id(id: int, db : Session= Depends(get_db)):
    transaction = transaction_service.show_transactions_by_id(id, db)    
    return transaction


