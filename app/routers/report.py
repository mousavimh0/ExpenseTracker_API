from fastapi import APIRouter, Depends
from app.schemas.transaction import BalanceResponse, TransactionResponse, TransactionCategory, TransactionType
from datetime import date
from app.services import report_service
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.db_models import TransactionDB

report_router = APIRouter()

@report_router.get("/", response_model = BalanceResponse)
def show_balance(db : Session = Depends(get_db) ):
    
    balance = report_service.calculate_balance(db)
    return balance


@report_router.get("/filter/period/{period}/{target_date}", response_model=list[TransactionResponse])
def filter_data_by_date(period: str, target_date: date,db : Session = Depends(get_db)):

    filtered_data = report_service.filtered_date(period= period, target_date=target_date, db= db)
    return filtered_data


@report_router.get("/filter/category", response_model=list[TransactionResponse])
def get_by_category(categroy: TransactionCategory, db : Session = Depends(get_db)):

    transactions = report_service.show_transactions_by_column(db= db , column= TransactionDB.category, value=categroy)
    return transactions


@report_router.get("/filter/type", response_model= list[TransactionResponse])
def get_by_type(type : TransactionType, db : Session = Depends(get_db)):

    transactions = report_service.show_transactions_by_column(db= db, column= TransactionDB.type , value= type)
    return transactions

@report_router.get("/filter/date" , response_model= list[TransactionResponse])
def get_by_date(date : date, db : Session = Depends(get_db)):
    transactions = report_service.show_transactions_by_column(db= db , column= TransactionDB.date , value=date)
    return transactions 