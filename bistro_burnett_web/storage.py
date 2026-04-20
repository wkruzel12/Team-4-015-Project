"""JSON persistence helpers for the Bistro Burnett web app."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: Path, default: Any) -> Any:
    """Load JSON data from disk and return a default value if missing."""
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
    """Persist returning customer profiles in a lightweight JSON file."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def get(self, phone: str) -> dict[str, str] | None:
        """Return one customer by phone number."""
        customers = load_json(self.path, {})
        return customers.get(phone)

    def save(self, phone: str, name: str) -> None:
        """Insert or update a customer profile."""
        customers = load_json(self.path, {})
        customers[phone] = {"phone": phone, "name": name}
        save_json(self.path, customers)


class OrderStore:
    """Persist submitted orders separately from the menu database."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def append(self, payload: dict[str, Any]) -> None:
        """Append a completed order snapshot to the JSON history file."""
        orders = load_json(self.path, [])
        orders.append(payload)
        save_json(self.path, orders)
