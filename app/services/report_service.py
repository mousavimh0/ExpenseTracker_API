from sqlalchemy.orm import Session
from app.repositories import report_repository
from datetime import date
from app.models.db_models import TransactionDB
from app.schemas.transaction import TransactionResponse, BalanceResponse
from fastapi import HTTPException
from app.redis import redis_client
import json


def to_response(transactions: TransactionDB):

    response_item = TransactionResponse(
        id=transactions.id,
        type=transactions.type,
        amount=transactions.amount,
        category=transactions.category,
        date_=transactions.date,
    )
    return response_item


def calculate_balance(db: Session, user_id: int):
    cache_key = f"report:balance:user:{user_id}"
    cashed_balance = redis_client.get(cache_key)
    if cashed_balance:
        # HIT
        print("cache hit")
        data = json.loads(cashed_balance)
        balancemodel = BalanceResponse(**data)
    else:
        # MISS
        print("cache miss")
        sum_income = report_repository.sum_amount("income", db, user_id)
        sum_expense = report_repository.sum_amount("expense", db, user_id)
        balance = sum_income - sum_expense
        balancemodel = BalanceResponse(
            income=sum_income, expense=sum_expense, balance=balance
        )
        cache_data = balancemodel.model_dump()
        cache_data = json.dumps(cache_data)
        redis_client.set(cache_key, cache_data, ex=60)
    return balancemodel


def filtered_date(period: str, target_date: date, db: Session, user_id: int):

    storage = report_repository.select_all(db, user_id)
    filtered = []
    for item in storage:
        item_date = date.fromisoformat(item.date_)

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

    if not filtered:
        raise HTTPException(404, "Transaction not found.")

    filtered_date = []
    for item in filtered:
        filtered_date.append(to_response(item))
    return filtered_date


def show_transactions_by_column(db: Session, column, value):
    transactions = report_repository.select_by_column(db, column, value)
    transactions_response = []
    for item in transactions:
        transactions_response.append(to_response(item))

    return transactions_response
