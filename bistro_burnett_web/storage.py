"""Bistro Burnett Web Prototype Storage Helpers

Date: April 2026
Authors: Team 4-015
Purpose:
    Persist returning customers and submitted orders outside the SQLite menu
    database using lightweight JSON files.
    Input: customer dictionaries, order dictionaries, and file paths.
    Output: saved JSON records loaded from or written to disk.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: Path, default: Any) -> Any:
    """Load JSON data from disk and return a default value if missing or invalid."""
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def save_json(path: Path, payload: Any) -> None:
    """Save JSON data to disk with stable formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


class CustomerStore:
    """Persist returning customer profiles in a lightweight JSON file.

    Input:
        A JSON file path plus customer phone/name values.
    Output:
        Readable customer records that can be reused on later visits.
    """

    def __init__(self, path: Path) -> None:
        self.path = path

    def get(self, phone: str) -> dict[str, str] | None:
        """Return one customer by phone number.

        Input:
            A phone number string.
        Output:
            A saved customer dictionary or ``None`` if no match exists.
        """
        customers = load_json(self.path, {})
        return customers.get(phone)

    def save(self, phone: str, name: str) -> None:
        """Insert or update a customer profile.

        Input:
            A phone number and customer name.
        Output:
            The JSON customer file is updated on disk.
        """
        customers = load_json(self.path, {})
        customers[phone] = {"phone": phone, "name": name}
        save_json(self.path, customers)


class OrderStore:
    """Persist submitted orders separately from the menu database.

    Input:
        A JSON file path and completed order payloads.
    Output:
        An appended order history file stored on disk.
    """

    def __init__(self, path: Path) -> None:
        self.path = path

    def append(self, payload: dict[str, Any]) -> None:
        """Append a completed order snapshot to the JSON history file.

        Input:
            A completed order dictionary.
        Output:
            The JSON order-history file is updated with one new record.
        """
        orders = load_json(self.path, [])
        orders.append(payload)
        save_json(self.path, orders)
