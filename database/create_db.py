import sqlite3

conn = sqlite3.connect("expenses.db")

cur = conn.cursor()

cur.execute(
    """  CREATE TABLE IF NOT EXISTS expenses
(ID INTEGER PRIMARY KEY,
Date DATE,
Description TEXT,
Category TEXT,
Account TEXT,
Amount REAL,
Type TEXT CHECK (Type IN ('debit', 'credit')))
"""
)

conn.commit()
conn.close()
