from fastapi import APIRouter, Depends
from app.schemas.transaction import Transaction, TransactionResponse
from app.services import transaction_service
from app.database import get_db
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user
from app.models.db_models import UserDB

transaction_router = APIRouter()


@transaction_router.post("/create", status_code=201)
def post_transaction(
    transaction: Transaction,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    new_transaction = transaction_service.add_transaction(
        transaction, db, current_user.id
    )
    return {"id": new_transaction.id, "type": new_transaction.type}


@transaction_router.get("/get", response_model=list[TransactionResponse])
def get_all_transactions(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    transactions = transaction_service.show_transactions(
        db, current_user.id, skip, limit
    )
    return transactions


@transaction_router.put("/update/{id}")
def put_transaction_by_id(
    transaction: Transaction,
    id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    updating_transaction = transaction_service.update_transaction(
        transaction, id, db, current_user.id
    )

    return updating_transaction


@transaction_router.delete("/delete/{id}")
def delete_transactions(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    transaction_service.delete_transaction(id, db, current_user.id)
    return {"message": "Transaction deleted successfully"}


@transaction_router.get("/get/{id}", response_model=TransactionResponse)
def get_transaction_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user),
):
    transaction = transaction_service.show_transactions_by_id(id, db, current_user.id)
    return transaction
