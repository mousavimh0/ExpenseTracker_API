import sqlite3

conn = sqlite3.connect("expenses.db" ,check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
               id INTEGER PRIMARY KEY,
               type TEXT,
               amount INTEGER,
               category TEXT,
               date TEXT)""")

conn.commit()

