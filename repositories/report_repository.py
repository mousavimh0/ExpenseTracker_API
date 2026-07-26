from sqlalchemy import select, func
from sqlalchemy.orm import Session
from db_models import TransactionDB
from fastapi import HTTPException

def sum_amount(type, db : Session):
    statement = select(func.sum(TransactionDB.amount)).where(TransactionDB.type == type)
    result = db.execute(statement).scalar()
    if result:
        return result
    else:
        raise HTTPException(404, "Transaction not found")
def select_all(db : Session)->list:
    
    statement = select(TransactionDB)
    result = db.execute(statement)
    transactions = result.scalars().all()
    if transactions:
        return transactions
    else:
        raise HTTPException(404, "Transaction not found")
    

def select_by_column(db : Session, column, value ):
    statement = select(TransactionDB).where(column == value )
    result = db.execute(statement)
    transactions = result.scalars().all()
    if transactions:
        return transactions
    else:
        raise HTTPException(404, "Transaction not found")    