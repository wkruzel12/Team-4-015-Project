"""Bistro Burnett Web Prototype Database Layer

Date: April 2026
Authors: Team 4-015
Purpose:
    Manage the SQLite menu database used by the Bistro Burnett prototype.
    Input: schema file contents, menu item payloads, and filter values.
    Output: seeded database tables, query results, and inserted or updated records.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path


BASES_SEED: list[tuple[str, str, str, float, float | None, int, int, str, int]] = [
    ("sandwiches", "size", '6"', 7.99, None, 0, 0, "Six inch made-to-order sandwich", 1),
    ("sandwiches", "size", '12"', 9.99, None, 0, 0, "Twelve inch made-to-order sandwich", 1),
    ("wraps", "size", "Wrap", 8.49, None, 0, 0, "Fresh wrap entree", 1),
    ("sandwiches", "bread", "Wheat", 0.0, None, 210, 8, "Fresh wheat bread", 1),
    ("sandwiches", "bread", "White", 0.0, None, 200, 7, "Classic white bread", 1),
    ("sandwiches", "bread", "Italian Herb on White", 0.0, None, 220, 8, "Italian herb seasoned bread", 1),
    ("sandwiches", "bread", "Jalapeno Cheddar on White", 0.0, None, 240, 9, "Bread with jalapeno cheddar flavor", 1),
    ("wraps", "bread", "Spinach Wrap", 0.0, None, 190, 7, "Spinach tortilla wrap", 1),
    ("wraps", "bread", "White Wrap", 0.0, None, 200, 7, "White tortilla wrap", 1),
    ("wraps", "bread", "Wheat Wrap", 0.0, None, 210, 8, "Wheat tortilla wrap", 1),
]

PROTEINS_SEED: list[tuple[str, str, float, float | None, int, int, str, int]] = [
    ("shared", "Hickory Smoked Turkey", 0.0, None, 50, 11, "Lean turkey protein", 1),
    ("shared", "Smoked Ham", 0.0, None, 60, 10, "Classic smoked ham", 1),
    ("shared", "Turkey, Ham Club & Bacon", 0.0, None, 120, 15, "Club blend with bacon", 1),
    ("shared", "Chicken Fajita", 0.0, None, 80, 13, "Seasoned chicken strips", 1),
    ("shared", "Italian", 0.0, None, 110, 12, "Italian deli blend", 1),
    ("shared", "Vegetarian", 0.0, None, 20, 2, "Vegetarian filling", 1),
]

CHEESES_SEED: list[tuple[str, str, float, float | None, int, int, str, int]] = [
    ("shared", "Cheddar", 0.0, None, 110, 7, "Cheddar cheese", 1),
    ("shared", "Provolone", 0.0, None, 100, 7, "Provolone cheese", 1),
    ("shared", "Pepper Jack", 0.0, None, 110, 7, "Pepper jack cheese", 1),
    ("shared", "Swiss", 0.0, None, 106, 8, "Swiss cheese", 1),
]

TOPPINGS_SEED: list[tuple[str, str, float, float | None, int, int, str, int]] = [
    ("shared", "Lettuce", 0.0, None, 5, 0, "Fresh lettuce", 1),
    ("shared", "Spinach", 0.0, None, 7, 1, "Fresh spinach", 1),
    ("shared", "Spring Mix", 0.0, None, 8, 1, "Spring mix greens", 1),
    ("shared", "Tomatoes", 0.0, None, 10, 0, "Sliced tomatoes", 1),
    ("shared", "Cucumbers", 0.0, None, 5, 0, "Cucumber slices", 1),
    ("shared", "Green Peppers", 0.0, None, 6, 0, "Green peppers", 1),
    ("shared", "Roasted Red Peppers", 0.0, None, 10, 0, "Roasted red peppers", 1),
    ("shared", "Red Onions", 0.0, None, 8, 0, "Red onions", 1),
    ("shared", "Shredded Carrots", 0.0, None, 12, 0, "Shredded carrots", 1),
    ("shared", "Black Olives", 0.0, None, 25, 0, "Black olives", 1),
    ("shared", "Pickles", 0.0, None, 5, 0, "Pickles", 1),
    ("shared", "Banana Peppers", 0.0, None, 5, 0, "Banana peppers", 1),
]

EXTRAS_SEED: list[tuple[str, str, str, float, float | None, int, int, str, int]] = [
    ("shared", "dressing", "Mayo", 0.0, None, 90, 0, "Mayonnaise", 1),
    ("shared", "dressing", "Ranch", 0.0, None, 110, 0, "Ranch dressing", 1),
    ("shared", "dressing", "Mustard", 0.0, None, 5, 0, "Mustard", 1),
    ("shared", "dressing", "Honey Mustard", 0.0, None, 40, 0, "Honey mustard", 1),
    ("shared", "dressing", "Creamy Italian", 0.0, None, 70, 0, "Creamy Italian dressing", 1),
    ("shared", "dressing", "Buffalo Sauce", 0.0, None, 10, 0, "Buffalo sauce", 1),
    ("shared", "dressing", "Chipotle", 0.0, None, 50, 0, "Chipotle dressing", 1),
    ("shared", "dressing", "Citrus BBQ", 0.0, None, 40, 0, "Citrus BBQ sauce", 1),
    ("shared", "dressing", "Oil & Vinegar", 0.0, None, 45, 0, "Oil and vinegar", 1),
    ("shared", "addon", "Extra Cheese", 1.00, 2.00, 110, 7, "Add extra cheese", 1),
    ("shared", "addon", "Extra Meat", 2.49, 3.69, 120, 15, "Add extra meat", 1),
    ("shared", "addon", "Avocado", 2.00, 2.99, 50, 1, "Add avocado", 1),
    ("shared", "addon", "Bacon", 2.00, 2.99, 80, 6, "Add bacon", 1),
]


class MenuDatabase:
    """Manage the five-table SQLite menu database.

    Input:
        A path to the SQLite database file and a path to the SQL schema file.
    Output:
        A reusable helper object that initializes, queries, inserts, and updates
        menu data for the Flask application.
    """

    def __init__(self, db_path: Path, schema_path: Path) -> None:
        """Store database paths and initialize the SQLite database if needed."""
        self.db_path = db_path
        self.schema_path = schema_path
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        """Open a SQLite connection and return rows as dictionary-like objects."""
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        """Create database objects from the schema and seed starter menu data."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.executescript(self.schema_path.read_text(encoding="utf-8"))
            self._seed_if_empty(connection)

    def _seed_if_empty(self, connection: sqlite3.Connection) -> None:
        """Insert starter menu records only when the database tables are empty."""
        if connection.execute("SELECT COUNT(*) FROM bases").fetchone()[0] == 0:
            connection.executemany(
                """
                INSERT INTO bases (
                    category, option_group, name, price, alt_price, calories, protein, description, active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                BASES_SEED,
            )
        if connection.execute("SELECT COUNT(*) FROM proteins").fetchone()[0] == 0:
            connection.executemany(
                """
                INSERT INTO proteins (
                    category, name, price, alt_price, calories, protein, description, active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                PROTEINS_SEED,
            )
        if connection.execute("SELECT COUNT(*) FROM cheeses").fetchone()[0] == 0:
            connection.executemany(
                """
                INSERT INTO cheeses (
                    category, name, price, alt_price, calories, protein, description, active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                CHEESES_SEED,
            )
        if connection.execute("SELECT COUNT(*) FROM toppings").fetchone()[0] == 0:
            connection.executemany(
                """
                INSERT INTO toppings (
                    category, name, price, alt_price, calories, protein, description, active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                TOPPINGS_SEED,
            )
        if connection.execute("SELECT COUNT(*) FROM extras").fetchone()[0] == 0:
            connection.executemany(
                """
                INSERT INTO extras (
                    category, extra_type, name, price, alt_price, calories, protein, description, active
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                EXTRAS_SEED,
            )

    def fetch_items(self, *, category: str | None = None, section: str | None = None, search: str = "", active_only: bool = False) -> list[dict]:
        """Fetch catalog rows with optional filters for the admin page.

        Input:
            Optional category, section, search text, and active-only flag.
        Output:
            A list of matching menu items represented as dictionaries.
        """
        query = "SELECT * FROM menu_catalog WHERE 1 = 1"
        params: list[object] = []
        if category:
            query += " AND category = ?"
            params.append(category)
        if section:
            query += " AND section = ?"
            params.append(section)
        if search:
            query += " AND (name LIKE ? OR description LIKE ?)"
            wildcard = f"%{search}%"
            params.extend([wildcard, wildcard])
        if active_only:
            query += " AND active = 1"
        query += " ORDER BY section, name"
        with self._connect() as connection:
            rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]

    def fetch_section_options(self, category: str, section: str) -> list[dict]:
        """Return active options for one order section and category.

        Input:
            The workflow category and the requested menu section.
        Output:
            A list of active menu items for that section.
        """
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM menu_catalog
                WHERE section = ?
                  AND active = 1
                  AND category IN (?, 'shared')
                ORDER BY name
                """,
                (section, category),
            ).fetchall()
        return [dict(row) for row in rows]

    def get_named_item(self, name: str, section: str) -> dict | None:
        """Return one named active catalog row.

        Input:
            A menu item name and section.
        Output:
            A matching menu item dictionary or ``None`` if not found.
        """
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT * FROM menu_catalog
                WHERE name = ? AND section = ? AND active = 1
                LIMIT 1
                """,
                (name, section),
            ).fetchone()
        return dict(row) if row else None

    def save_item(self, item_id: str | None, payload: dict[str, object]) -> None:
        """Insert or update a menu row in the correct table.

        Input:
            An optional item id and a payload dictionary from the admin form.
        Output:
            The SQLite table is updated with a new or modified record.
        """
        table, pk_name, subtype_field, subtype_value, record_id = self._resolve_storage(payload["section"], item_id)
        assignments = {
            "category": payload["category"],
            "name": payload["name"],
            "price": payload["price"],
            "alt_price": payload["alt_price"],
            "calories": payload["calories"],
            "protein": payload["protein"],
            "description": payload["description"],
            "active": int(payload["active"]),
        }
        if subtype_field:
            assignments[subtype_field] = subtype_value

        with self._connect() as connection:
            if record_id is None:
                columns = ", ".join(assignments.keys())
                placeholders = ", ".join("?" for _ in assignments)
                connection.execute(
                    f"INSERT INTO {table} ({columns}) VALUES ({placeholders})",
                    list(assignments.values()),
                )
            else:
                set_clause = ", ".join(f"{column} = ?" for column in assignments)
                values = list(assignments.values()) + [record_id]
                connection.execute(
                    f"UPDATE {table} SET {set_clause} WHERE {pk_name} = ?",
                    values,
                )

    def report_stats(self) -> dict[str, object]:
        """Return summary statistics for the menu database.

        Input:
            None.
        Output:
            A dictionary of item counts and average pricing information.
        """
        items = self.fetch_items()
        categories: dict[str, int] = {}
        for item in items:
            categories[item["category"]] = categories.get(item["category"], 0) + 1
        average_price = sum(item["price"] for item in items) / len(items) if items else 0
        return {
            "total_items": len(items),
            "active_items": sum(1 for item in items if item["active"]),
            "average_price": average_price,
            "category_counts": categories,
        }

    def _resolve_storage(self, section: str, item_id: str | None) -> tuple[str, str, str | None, str | None, int | None]:
        """Map a logical menu section to the correct SQLite table and key metadata."""
        if section in {"entree", "bread"}:
            table, pk_name, subtype_field, subtype_value = "bases", "base_id", "option_group", "size" if section == "entree" else "bread"
        elif section == "protein":
            table, pk_name, subtype_field, subtype_value = "proteins", "protein_id", None, None
        elif section == "cheese":
            table, pk_name, subtype_field, subtype_value = "cheeses", "cheese_id", None, None
        elif section == "topping":
            table, pk_name, subtype_field, subtype_value = "toppings", "topping_id", None, None
        else:
            table, pk_name, subtype_field, subtype_value = "extras", "extra_id", "extra_type", section

        record_id: int | None = None
        if item_id:
            prefix, _, suffix = item_id.partition(":")
            if prefix:
                table = prefix
                pk_name = {
                    "bases": "base_id",
                    "proteins": "protein_id",
                    "cheeses": "cheese_id",
                    "toppings": "topping_id",
                    "extras": "extra_id",
                }[table]
            record_id = int(suffix) if suffix else int(item_id)
        return table, pk_name, subtype_field, subtype_value, record_id
