import sqlite3

DB_NAME = "expenses.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            transaction_date TEXT NOT NULL,
            note TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_transaction(transaction_type, category, amount, transaction_date, note):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
                   
        INSERT INTO transactions
        (transaction_type, category, amount, transaction_date, note)
        VALUES (?, ?, ?, ?, ?) 
            
    """, (transaction_type, category, amount, transaction_date, note))
    conn.commit()
    conn.close()

def get_all_transactions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, transaction_type, category, amount, transaction_date, note
        FROM transactions
        ORDER BY transaction_date DESC, id DESC
    """)
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def delete_transaction(transaction_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM transactions
        WHERE id = ?
    """, (transaction_id,))
    conn.commit()
    conn.close()
