"""Bistro Burnett Online Ordering System.

Simple Flask web prototype for a class project.
This file contains Flask routes and application setup.
"""

from flask import Flask, flash, redirect, render_template, request, session, url_for

from database import (
    get_customer_name_by_phone,
    get_orders,
    init_db,
    insert_order,
    update_order_status,
)
from models import Order
from utils import (
    format_currency,
    format_list_for_display,
    get_menu_options,
    parse_multi_select,
    validate_category,
    validate_customer_name,
    validate_order_form,
    validate_phone_number,
)

app = Flask(__name__)
app.secret_key = "bistro-burnett-class-project-secret"


@app.route("/")
def index():
    """Show start page where user enters phone number."""
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start_order():
    """Validate phone number and start workflow."""
    phone_number = request.form.get("phone_number", "").strip()
    is_valid, error_message = validate_phone_number(phone_number)

    if is_valid:
        session["phone_number"] = phone_number
        existing_name = get_customer_name_by_phone(phone_number)
        session["existing_name"] = existing_name if existing_name else ""
        return redirect(url_for("customer_info"))

    flash(error_message, "error")
    return redirect(url_for("index"))


@app.route("/customer", methods=["GET", "POST"])
def customer_info():
    """Capture customer name (prefill for returning customer)."""
    if "phone_number" not in session:
        flash("Please start your order first.", "error")
        return redirect(url_for("index"))

    prefill_name = session.get("existing_name", "")

    if request.method == "POST":
        customer_name = request.form.get("customer_name", "").strip()
        is_valid, error_message = validate_customer_name(customer_name)

        if is_valid:
            session["customer_name"] = customer_name
            return redirect(url_for("category"))

        flash(error_message, "error")
        return render_template("customer_info.html", prefill_name=customer_name)

    return render_template("customer_info.html", prefill_name=prefill_name)


@app.route("/category", methods=["GET", "POST"])
def category():
    """Choose Sandwich or Wrap category."""
    if "customer_name" not in session:
        flash("Please complete customer information first.", "error")
        return redirect(url_for("customer_info"))

    if request.method == "POST":
        selected_category = request.form.get("category", "").strip()
        is_valid, error_message = validate_category(selected_category)

        if is_valid:
            session["category"] = selected_category
            return redirect(url_for("build_order"))

        flash(error_message, "error")

    return render_template("category.html", selected_category=session.get("category", ""))


@app.route("/build", methods=["GET", "POST"])
def build_order():
    """Build order and show live summary + total."""
    if "category" not in session:
        flash("Please choose a category first.", "error")
        return redirect(url_for("category"))

    menu_options = get_menu_options(session.get("category", ""))

    # Default form values.
    form_data = {
        "size": "",
        "bread_or_tortilla": "",
        "protein": "",
        "cheese": "",
        "toppings": [],
        "dressings": [],
        "addons": [],
    }

    summary = None
    running_total = 0.0

    if request.method == "POST":
        form_data["size"] = request.form.get("size", "").strip()
        form_data["bread_or_tortilla"] = request.form.get("bread_or_tortilla", "").strip()
        form_data["protein"] = request.form.get("protein", "").strip()
        form_data["cheese"] = request.form.get("cheese", "").strip()
        form_data["toppings"] = parse_multi_select(request.form.getlist("toppings"))
        form_data["dressings"] = parse_multi_select(request.form.getlist("dressings"))
        form_data["addons"] = parse_multi_select(request.form.getlist("addons"))

        is_valid, error_message = validate_order_form(form_data)

        # Create Order object so user can see summary/price even before final submit.
        temp_order = Order(
            phone_number=session.get("phone_number", ""),
            customer_name=session.get("customer_name", ""),
            category=session.get("category", ""),
            size=form_data["size"],
            bread_or_tortilla=form_data["bread_or_tortilla"],
            protein=form_data["protein"],
            cheese=form_data["cheese"],
            toppings=form_data["toppings"],
            dressings=form_data["dressings"],
            addons=form_data["addons"],
        )

        running_total = temp_order.calculate_total()
        summary = temp_order.format_summary()

        if is_valid:
            session["order_data"] = {
                "size": form_data["size"],
                "bread_or_tortilla": form_data["bread_or_tortilla"],
                "protein": form_data["protein"],
                "cheese": form_data["cheese"],
                "toppings": ", ".join(form_data["toppings"]),
                "dressings": ", ".join(form_data["dressings"]),
                "addons": ", ".join(form_data["addons"]),
                "total_price": running_total,
            }
            return redirect(url_for("review_order"))

        flash(error_message, "error")

    return render_template(
        "build_order.html",
        category=session.get("category", ""),
        menu_options=menu_options,
        form_data=form_data,
        running_total=format_currency(running_total),
        summary=summary,
    )


@app.route("/review")
def review_order():
    """Show order details and allow user to continue or edit."""
    order_data = session.get("order_data")
    if not order_data:
        flash("Please build your order first.", "error")
        return redirect(url_for("build_order"))

    return render_template(
        "review_order.html",
        phone_number=session.get("phone_number", ""),
        customer_name=session.get("customer_name", ""),
        category=session.get("category", ""),
        order_data=order_data,
        format_list_for_display=format_list_for_display,
        total_display=format_currency(order_data.get("total_price", 0.0)),
    )


@app.route("/payment", methods=["GET", "POST"])
def payment():
    """Show payment notice and submit order to database."""
    order_data = session.get("order_data")
    if not order_data:
        flash("Please build and review your order first.", "error")
        return redirect(url_for("build_order"))

    if request.method == "POST":
        order = Order(
            phone_number=session.get("phone_number", ""),
            customer_name=session.get("customer_name", ""),
            category=session.get("category", ""),
            size=order_data.get("size", ""),
            bread_or_tortilla=order_data.get("bread_or_tortilla", ""),
            protein=order_data.get("protein", ""),
            cheese=order_data.get("cheese", ""),
            toppings=parse_multi_select(order_data.get("toppings", "").split(",")),
            dressings=parse_multi_select(order_data.get("dressings", "").split(",")),
            addons=parse_multi_select(order_data.get("addons", "").split(",")),
            status="Received",
        )
        order_id = insert_order(order)
        session["latest_order_id"] = order_id
        return redirect(url_for("confirmation"))

    return render_template(
        "payment.html",
        phone_number=session.get("phone_number", ""),
        customer_name=session.get("customer_name", ""),
        category=session.get("category", ""),
        order_data=order_data,
        total_display=format_currency(order_data.get("total_price", 0.0)),
    )


@app.route("/confirmation")
def confirmation():
    """Show confirmation and clear workflow session data."""
    customer_name = session.get("customer_name", "Customer")
    latest_order_id = session.get("latest_order_id", "N/A")

    # Keep only minimal confirmation info; clear rest for new order.
    session.pop("phone_number", None)
    session.pop("existing_name", None)
    session.pop("customer_name", None)
    session.pop("category", None)
    session.pop("order_data", None)

    return render_template(
        "confirmation.html",
        customer_name=customer_name,
        latest_order_id=latest_order_id,
    )


@app.route("/orders", methods=["GET", "POST"])
def orders_management():
    """Display saved orders, filter by phone, and update status."""
    if request.method == "POST":
        order_id_text = request.form.get("order_id", "").strip()
        new_status = request.form.get("status", "").strip()
        if order_id_text.isdigit() and new_status in ["Received", "In Progress", "Complete"]:
            update_order_status(int(order_id_text), new_status)
            flash("Order status updated successfully.", "success")
        else:
            flash("Invalid status update request.", "error")

        return redirect(url_for("orders_management", phone_filter=request.args.get("phone_filter", "")))

    phone_filter = request.args.get("phone_filter", "").strip()
    orders = get_orders(phone_filter=phone_filter)

    return render_template(
        "orders.html",
        orders=orders,
        phone_filter=phone_filter,
        format_currency=format_currency,
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
