from fastapi import HTTPException
from models import Transaction
from repositories import transaction_repository

def show_transactions()->list:
    rows = transaction_repository.select_all()
    response_list = []
    for item in rows:
        response_list.append(
            {
                "id": item[0],
                "type": item[1],
                "amount": item[2],
                "category": item[3],
                "date_": item[4],
            }
        )

    return response_list


def ensure_transaction_exists(id : int)->bool:
    result = transaction_repository.exist_by_id(id)
    if result is None:
        raise HTTPException(status_code=404, detail="id not found")
    return True


def add_transaction(transaction: Transaction):
    transaction_repository.insert_transaction(transaction)


def update_transaction(transaction : Transaction, id: int):

    ensure_transaction_exists(id)
    transaction_repository.update_transaction(transaction, id)


def delete_transaction(id: int):
    ensure_transaction_exists(id)
    transaction_repository.delete_transaction(id)


def show_transactions_by_id(id:int)->dict:
    row = transaction_repository.select_row_by_id(id)
    if row is None:
        raise HTTPException(status_code=404, detail="id not found")
    response_items = {
                "id": row[0],
                "type": row[1],
                "amount": row[2],
                "category": row[3],
                "date_": row[4],
            }
    return response_items

