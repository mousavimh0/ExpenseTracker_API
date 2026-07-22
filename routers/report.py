from fastapi import APIRouter, HTTPException
from services import transaction_service
from models import Transaction,BalanceResponse, TransactionResponse, TransactionCategory, TransactionType
from datetime import date
from database import conn, cursor



report_router = APIRouter()

def sum_by_sql(type):
    cursor.execute("""SELECT sum(amount) from transactions
                   WHERE type = ?""",
                   (type,))
    row = cursor.fetchone()
    for i in row:
        return int(i)

def get_list_from_database():
    rows = cursor.fetchall()
    if not rows:
        raise HTTPException(404 ,"item not found.")
    transactions = []
    for tran in rows :
        transactions.append(TransactionResponse(id =tran[0], type = tran[1], amount = tran[2], category= tran[3], date_= tran[4]))
    return transactions



@report_router.get("/" , response_model= BalanceResponse)
def show_balance():
    
    sum_income = sum_by_sql("income")
    
    sum_expense = sum_by_sql("expense")

    balance = sum_income - sum_expense

    return {
        "income" : sum_income,
        "expense" : sum_expense,
        "balance" : balance
    }


@report_router.get("/filter/period/{period}/{target_date}", response_model=list[TransactionResponse])
def filtered_date(period: str, target_date: date):

    storage = transaction_service.show_transactions()
    filtered = []
    for item in storage:
        item_date = date.fromisoformat(item["date_"])

        if period == "all":
            filtered.append(item)

        if period == "monthly":
            if (
                item_date.month == target_date.month
                and item_date.year == target_date.year
            ):
                filtered.append(item)

        if period == "weekly":
            today = date.today()
            difference = (today - item_date).days
            if difference <= 7:
                filtered.append(item)

    return filtered

@report_router.get("/filter/category", response_model=list[TransactionResponse])
def get_by_category(categroy: TransactionCategory):

    cursor.execute(
        """SELECT * from transactions
                   WHERE category = ?""",
        (categroy,),
    )

    transactions = get_list_from_database()
    return transactions

@report_router.get("/filter/type", response_model= list[TransactionResponse])
def get_by_type(type : TransactionType):
    cursor.execute(
            """SELECT * from transactions
            WHERE type = ?""",
            (type,),
        )

    transactions = get_list_from_database()
    return transactions

@report_router.get("/filter/date" , response_model= list[TransactionResponse])
def get_by_date(date : date):
    cursor.execute("""SELECT * FROM transactions
                   WHERE date = ?""",
                   (date, ))
    transactions = get_list_from_database()
    return transactions 