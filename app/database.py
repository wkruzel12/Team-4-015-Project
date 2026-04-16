import sqlite3
import os

# Save the database in the existing 'data' folder for organization
DB_PATH = os.path.join(os.path.dirname(__file__), '../data/bistro.db')

def get_db_connection():
    """Establishes connection to SQLite database[cite: 46]."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Creates the table with at least 5 fields[cite: 47, 133]."""
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT,
        name TEXT,
        category TEXT,
        details TEXT,
        total REAL,
        status TEXT
    )''')
    conn.commit()
    conn.close()

def insert_order(order_data):
    """Database Operation: Insert[cite: 50, 134]."""
    conn = get_db_connection()
    conn.execute('INSERT INTO orders (phone, name, category, details, total, status) VALUES (?, ?, ?, ?, ?, ?)',
                 (order_data['phone'], order_data['name'], order_data['cat'], 
                  order_data['details'], order_data['total'], 'Received'))
    conn.commit()
    conn.close()
