"""Bistro Burnett Web Prototype

Date: April 2026
Authors: Team 4-015
Purpose:
    Define the Flask routes, validation rules, workflow state, and pricing logic
    for the Bistro Burnett ordering application.
    Input: browser form submissions and session state.
    Output: rendered HTML pages, updated order data, and persisted order records.
"""

from __future__ import annotations

import os
import re
from datetime import datetime
from pathlib import Path
from secrets import token_hex

from flask import Flask, flash, redirect, render_template, request, session, url_for

from .db import MenuDatabase
from .storage import CustomerStore, OrderStore


UNSET = "__unset__"


def create_app() -> Flask:
    """Create and configure the Flask application object.

    Input:
        None directly. The function reads template/static paths and local data file
        locations from the project folder.
    Output:
        A configured Flask application with routes, session support, and storage
        dependencies attached through closures.
    """
    app = Flask(__name__, template_folder=str(Path(__file__).resolve().parent.parent / "templates"), static_folder=str(Path(__file__).resolve().parent.parent / "static"))
    app.secret_key = os.environ.get("FLASK_SECRET_KEY", token_hex(16))

    root = Path(__file__).resolve().parent.parent
    menu_db = MenuDatabase(root / "data" / "menu.db", root / "data" / "schema.sql")
    customer_store = CustomerStore(root / "data" / "customers.json")
    order_store = OrderStore(root / "data" / "orders.json")

    def default_order() -> dict:
        """Return the default order state used for a new workflow session."""
        return {
            "category": None,
            "size": "",
            "bread": "",
            "protein": "",
            "cheese": "",
            "toppings": [],
            "dressings": [],
            "addons": [],
            "payment_method": "Campus Cash Card",
        }

    def current_order() -> dict:
        """Return the current order from session storage, creating it if missing."""
        order = session.get("order")
        if not order:
            order = default_order()
            session["order"] = order
        return order

    def reset_order() -> None:
        """Reset the in-progress order back to the default blank state."""
        session["order"] = default_order()

    def current_customer() -> dict:
        """Return the current customer from session storage, creating it if missing."""
        customer = session.get("customer")
        if not customer:
            customer = {"name": "", "phone": ""}
            session["customer"] = customer
        return customer

    def base_description(order: dict) -> str:
        """Build a readable base description string for the review screens."""
        if order["category"] == "sandwiches":
            return f'{order["size"]} Sandwich on {order["bread"]}'.strip()
        if order["category"] == "wraps":
            return f'{order["bread"]} Wrap'.strip()
        return ""

    def calculate_total(order: dict) -> float:
        """Calculate the order total using SQLite-backed menu pricing rules."""
        total = 0.0
        if order["category"] == "sandwiches" and order["size"]:
            entree = menu_db.get_named_item(order["size"], "entree")
            total += entree["price"] if entree else 0
        elif order["category"] == "wraps":
            entree = menu_db.get_named_item("Wrap", "entree")
            total += entree["price"] if entree else 0

        for addon_name in order["addons"]:
            addon = menu_db.get_named_item(addon_name, "addon")
            if not addon:
                continue
            if order["category"] == "sandwiches" and order["size"] == '12"' and addon["alt_price"] is not None:
                total += addon["alt_price"]
            else:
                total += addon["price"]
        return total

    def summary_rows(order: dict) -> list[tuple[str, str]]:
        """Return label/value pairs used by the order summary panels."""
        return [
            ("Base", base_description(order)),
            ("Protein", order["protein"]),
            ("Cheese", order["cheese"]),
            ("Toppings", ", ".join(order["toppings"])),
            ("Dressings", ", ".join(order["dressings"])),
            ("Add-ons", ", ".join(order["addons"])),
        ]

    @app.context_processor
    def inject_globals() -> dict:
        """Expose shared summary and progress data to every rendered template."""
        order = current_order()
        progress_steps = [
            ("welcome", "Welcome"),
            ("category", "Category"),
            ("build_order", "Build"),
            ("review_order", "Review"),
            ("customer_info", "Info"),
            ("payment", "Payment"),
            ("confirmation", "Complete"),
        ]
        step_lookup = {name: index + 1 for index, (name, _label) in enumerate(progress_steps)}
        return {
            "current_step": request.endpoint,
            "progress_steps": progress_steps,
            "active_step_index": step_lookup.get(request.endpoint, 1),
            "order_summary_rows": summary_rows(order),
            "order_total": f"${calculate_total(order):.2f}",
            "customer_name": current_customer().get("name", ""),
        }

    @app.route("/", methods=["GET", "POST"])
    def welcome():
        """Handle the first workflow step: phone lookup and returning-customer check."""
        customer = current_customer()
        if request.method == "POST":
            raw_phone = request.form.get("phone", "").strip()
            digits = re.sub(r"\D", "", raw_phone)
            pattern = re.compile(r"^(\(\d{3}\)\s?\d{3}-?\d{4}|\d{3}[-\s]?\d{3}[-\s]?\d{4})$")
            if not raw_phone or len(digits) != 10 or not pattern.match(raw_phone):
                flash("Use (123) 456-7890, 123-456-7890, or 123 456 7890.", "error")
                return render_template("welcome.html", phone=raw_phone)

            customer["phone"] = digits
            session["customer"] = customer
            existing = customer_store.get(digits)
            if existing:
                customer["name"] = existing["name"]
                session["customer"] = customer
                return redirect(url_for("category"))
            return redirect(url_for("name_entry"))
        return render_template("welcome.html", phone=customer.get("phone", ""))

    @app.route("/name-entry", methods=["GET", "POST"])
    def name_entry():
        """Collect and validate the customer name for new users."""
        customer = current_customer()
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            if not name:
                flash("Name is required.", "error")
                return render_template("name_entry.html", name=name)
            if len(name) < 2 or not re.fullmatch(r"[A-Za-z\s\-']+", name):
                flash("Use at least 2 letters and only letters, spaces, hyphens, or apostrophes.", "error")
                return render_template("name_entry.html", name=name)

            customer["name"] = name
            session["customer"] = customer
            customer_store.save(customer["phone"], name)
            return redirect(url_for("category"))
        return render_template("name_entry.html", name=customer.get("name", ""))

    @app.route("/category", methods=["GET", "POST"])
    def category():
        """Let the user choose the sandwich or wrap ordering workflow."""
        customer = current_customer()
        if request.method == "POST":
            choice = request.form.get("category")
            if choice not in {"sandwiches", "wraps"}:
                flash("Please choose Sandwiches or Wraps.", "error")
            else:
                reset_order()
                order = current_order()
                order["category"] = choice
                session["order"] = order
                return redirect(url_for("build_order"))
        return render_template("category.html", customer_name=customer.get("name", ""))

    @app.route("/build", methods=["GET", "POST"])
    def build_order():
        """Collect menu selections and validate the build-order step."""
        order = current_order()
        if not order["category"]:
            return redirect(url_for("category"))

        entree_items = menu_db.fetch_section_options(order["category"], "entree")
        bread_items = menu_db.fetch_section_options(order["category"], "bread")
        protein_items = menu_db.fetch_section_options(order["category"], "protein")
        cheese_items = menu_db.fetch_section_options(order["category"], "cheese")
        topping_items = menu_db.fetch_section_options(order["category"], "topping")
        dressing_items = menu_db.fetch_section_options(order["category"], "dressing")
        addon_items = menu_db.fetch_section_options(order["category"], "addon")

        if request.method == "POST":
            order["size"] = "" if request.form.get("size") == UNSET else request.form.get("size", "")
            order["bread"] = request.form.get("bread", "")
            order["protein"] = "" if request.form.get("protein") == UNSET else request.form.get("protein", "")
            cheese = request.form.get("cheese", UNSET)
            order["cheese"] = "" if cheese == UNSET else cheese
            order["toppings"] = request.form.getlist("toppings")
            order["dressings"] = request.form.getlist("dressings")
            order["addons"] = request.form.getlist("addons")
            session["order"] = order

            if order["category"] == "sandwiches" and not order["size"]:
                flash("Please choose a sandwich size.", "error")
            elif not order["bread"] or not order["protein"]:
                flash("Please choose a bread or wrap and a protein.", "error")
            else:
                return redirect(url_for("review_order"))

        return render_template(
            "build_order.html",
            order=order,
            unset=UNSET,
            entree_items=entree_items,
            bread_items=bread_items,
            protein_items=protein_items,
            cheese_items=cheese_items,
            topping_items=topping_items,
            dressing_items=dressing_items,
            addon_items=addon_items,
        )

    @app.route("/review")
    def review_order():
        """Display the saved order selections and computed total before checkout."""
        order = current_order()
        if not order["category"]:
            return redirect(url_for("category"))
        return render_template("review_order.html", order=order, base_description=base_description(order), total=f"${calculate_total(order):.2f}")

    @app.route("/customer-info", methods=["GET", "POST"])
    def customer_info():
        """Confirm the customer information before payment."""
        customer = current_customer()
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            if not name:
                flash("Please enter your name before continuing.", "error")
            else:
                customer["name"] = name
                session["customer"] = customer
                customer_store.save(customer["phone"], name)
                return redirect(url_for("payment"))
        return render_template("customer_info.html", customer=customer)

    @app.route("/payment", methods=["GET", "POST"])
    def payment():
        """Capture payment choice and store the completed order snapshot."""
        order = current_order()
        if request.method == "POST":
            order["payment_method"] = request.form.get("payment_method", "Campus Cash Card")
            session["order"] = order
            order_number = f"BB-{datetime.now().strftime('%H%M%S')}"
            session["order_number"] = order_number
            order_store.append(
                {
                    "order_number": order_number,
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "customer": current_customer(),
                    "order": order,
                    "total": round(calculate_total(order), 2),
                }
            )
            return redirect(url_for("confirmation"))
        return render_template("payment.html", payment_method=order.get("payment_method", "Campus Cash Card"))

    @app.route("/confirmation", methods=["GET", "POST"])
    def confirmation():
        """Show the final confirmation page and optionally restart the workflow."""
        if request.method == "POST":
            session["customer"] = {"name": "", "phone": ""}
            reset_order()
            session.pop("order_number", None)
            return redirect(url_for("welcome"))
        return render_template("confirmation.html", order_number=session.get("order_number", "BB-000000"))

    @app.route("/menu-admin", methods=["GET", "POST"])
    def menu_admin():
        """Provide a simple admin interface for SQLite menu browsing and updates."""
        if request.method == "POST":
            form = request.form
            try:
                payload = {
                    "category": form.get("category", "shared"),
                    "section": form.get("section", "protein"),
                    "name": form.get("name", "").strip(),
                    "price": float(form.get("price") or 0),
                    "alt_price": float(form["alt_price"]) if form.get("alt_price", "").strip() else None,
                    "calories": int(form.get("calories") or 0),
                    "protein": int(form.get("protein") or 0),
                    "description": form.get("description", "").strip() or "Menu item",
                    "active": form.get("active") == "on",
                }
            except ValueError:
                flash("Price, alt price, calories, and protein must be valid numbers.", "error")
            else:
                if not payload["name"]:
                    flash("Menu items must have a name.", "error")
                else:
                    menu_db.save_item(form.get("item_id") or None, payload)
                    flash("Menu item saved.", "success")
                    return redirect(url_for("menu_admin"))

        filters = {
            "category": request.args.get("category", ""),
            "section": request.args.get("section", ""),
            "search": request.args.get("search", ""),
        }
        return render_template(
            "menu_admin.html",
            items=menu_db.fetch_items(
                category=filters["category"] or None,
                section=filters["section"] or None,
                search=filters["search"].strip(),
            ),
            filters=filters,
            stats=menu_db.report_stats(),
        )

    return app
