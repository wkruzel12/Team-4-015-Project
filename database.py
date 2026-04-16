"""Database helpers for Bistro Burnett.

Contains SQLite connection, table creation, and CRUD operations.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path("data") / "bistro_burnett.db"


def get_connection():
    """Create and return a SQLite connection with row factory."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create orders table if it does not already exist."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            category TEXT NOT NULL,
            size TEXT NOT NULL,
            bread_or_tortilla TEXT NOT NULL,
            protein TEXT NOT NULL,
            cheese TEXT,
            toppings TEXT,
            dressings TEXT,
            addons TEXT,
            total_price REAL NOT NULL,
            status TEXT NOT NULL
        )
        """
    )
    connection.commit()
    connection.close()


def insert_order(order):
    """Insert one order into the database and return the new order ID."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO orders (
            phone_number,
            customer_name,
            category,
            size,
            bread_or_tortilla,
            protein,
            cheese,
            toppings,
            dressings,
            addons,
            total_price,
            status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            order.phone_number,
            order.customer_name,
            order.category,
            order.size,
            order.bread_or_tortilla,
            order.protein,
            order.cheese,
            ", ".join(order.toppings),
            ", ".join(order.dressings),
            ", ".join(order.addons),
            order.calculate_total(),
            order.status,
        ),
    )
    connection.commit()
    new_id = cursor.lastrowid
    connection.close()
    return new_id


def get_orders(phone_filter=""):
    """Retrieve all orders or filter by phone number (partial match)."""
    connection = get_connection()
    cursor = connection.cursor()

    if phone_filter:
        cursor.execute(
            """
            SELECT *
            FROM orders
            WHERE phone_number LIKE ?
            ORDER BY order_id DESC
            """,
            (f"%{phone_filter}%",),
        )
    else:
        cursor.execute(
            """
            SELECT *
            FROM orders
            ORDER BY order_id DESC
            """
        )

    rows = cursor.fetchall()
    connection.close()

    order_list = []
    for row in rows:
        order_list.append(dict(row))
    return order_list


def update_order_status(order_id, new_status):
    """Update the status value for a specific order."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        UPDATE orders
        SET status = ?
        WHERE order_id = ?
        """,
        (new_status, order_id),
    )
    connection.commit()
    connection.close()


def get_customer_name_by_phone(phone_number):
    """Find most recent customer name by phone number for returning users."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT customer_name
        FROM orders
        WHERE phone_number = ?
        ORDER BY order_id DESC
        LIMIT 1
        """,
        (phone_number,),
    )
    row = cursor.fetchone()
    connection.close()

    if row:
        return row["customer_name"]
    return ""
