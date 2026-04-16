# SQLite Connection and CRUD Operations

import sqlite3

class Database:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, item TEXT, price REAL)''')
        self.connection.commit()

    def insert_order(self, item, price):
        self.cursor.execute('''INSERT INTO orders (item, price) VALUES (?, ?)''', (item, price))
        self.connection.commit()

    def fetch_orders(self):
        self.cursor.execute('''SELECT * FROM orders''')
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()
