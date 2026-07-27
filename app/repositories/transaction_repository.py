from app.schemas.models import Transaction
from app.models.db_models import TransactionDB
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import select

def select_all(db : Session)->list:
    
    statement = select(TransactionDB)
    result = db.execute(statement)
    transactions = result.scalars().all()
    return transactions
    

def select_transaction_by_id(id, db : Session):
   
    statement = select(TransactionDB).where(TransactionDB.id == id)
    transaction = db.execute(statement).scalar_one_or_none()
    if transaction:
        return transaction
    else: 
            raise HTTPException(404, detail="Transaction not found.")


    
def insert_transaction(transaction : Transaction, db : Session):
    new_transaction = TransactionDB(
        type = transaction.type,
        amount = transaction.amount,
        category = transaction.category,
        date = transaction.date_
    )
    db.add(new_transaction)
    db.commit()


def update_transaction(transaction : Transaction, id, db : Session):
    statement = select(TransactionDB).where(TransactionDB.id == id)
    result = db.execute(statement)
    updating_transaction = result.scalar_one_or_none()

    if updating_transaction:
        updating_transaction.type = transaction.type
        updating_transaction.amount = transaction.amount
        updating_transaction.category = transaction.category
        updating_transaction.date = transaction.date_
        
        db.commit()
    else: 
        raise HTTPException(404, detail="Transaction not found.")
    

def delete_transaction(id, db : Session):
    statement = select(TransactionDB).where(TransactionDB.id == id)
    transaction = db.execute(statement).scalar_one_or_none()
    
    if transaction:
        db.delete(transaction)
        db.commit()
    else: 
            raise HTTPException(404, detail="Transaction not found.")
    

    