from database import cursor, conn
from models import Transaction

def select_all()->list:
    cursor.execute("""SELECT * FROM transactions""")
    rows = cursor.fetchall()
    return rows


def exist_by_id(id):
    cursor.execute(
        """SELECT 1 From transactions
                   WHERE id = ?""",
        (id,),
    )
    result = cursor.fetchone()
    return result


def insert_transaction(transaction : Transaction):
    cursor.execute(
        """INSERT INTO transactions (type, amount, category, date)
                   VALUES(?, ?, ?, ?)""",
        (transaction.type, transaction.amount, transaction.category, transaction.date_),
    )
    conn.commit()


def update_transaction(transaction : Transaction, id):
    cursor.execute(
        """UPDATE transactions
                   SET type = ?, amount = ?, category = ?, date = ?
                   WHERE id = ?""",
        (
            transaction.type,
            transaction.amount,
            transaction.category,
            transaction.date_,
            id,
        ),
    )
    conn.commit()


def delete_transaction(id):
    cursor.execute(
        """DELETE FROM transactions 
                   WHERE id = ?""",
        (id,),
    )
    conn.commit()

def select_row_by_id(id):
    cursor.execute(
        """SELECT * FROM transactions
                   WHERE id = ?""",
        (id,),
    )
    row = cursor.fetchone()
    return row