from fastapi import FastAPI
from models import Transaction, TransactionCategory, TransactionType
from models import TransactionResponse , BalanceResponse
from database import conn
from database import cursor
from fastapi import HTTPException
from datetime import date
from routers.transactions import transaction_router
from routers.report import report_router

app = FastAPI()

app.include_router(router= transaction_router ,prefix= "/transactions")
app.include_router(router= report_router, prefix="/report")
