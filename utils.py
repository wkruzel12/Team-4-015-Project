"""Utility functions for validation, pricing display, and menu setup."""

import re


def validate_phone_number(phone_number):
    """Validate phone number.

    Input: phone_number (str)
    Output: (bool, str)
    """
    if not phone_number:
        return False, "Phone number is required."

    if not phone_number.isdigit():
        return False, "Phone number must contain numbers only."

    if len(phone_number) != 10:
        return False, "Phone number must be exactly 10 digits."

    return True, ""


def validate_customer_name(customer_name):
    """Validate customer name format for beginner-friendly form rules."""
    if not customer_name:
        return False, "Customer name is required."

    if len(customer_name) < 2:
        return False, "Customer name must be at least 2 characters."

    if not re.fullmatch(r"[A-Za-z ]+", customer_name):
        return False, "Name should use letters and spaces only."

    return True, ""


def validate_category(category):
    """Validate category selection (Sandwich or Wrap)."""
    if category not in ["Sandwich", "Wrap"]:
        return False, "Please choose Sandwich or Wrap before continuing."
    return True, ""


def validate_order_form(form_data):
    """Validate required order fields using if/elif/else structure."""
    if not form_data.get("size"):
        return False, "Please choose a size."
    elif not form_data.get("bread_or_tortilla"):
        return False, "Please choose bread or tortilla."
    elif not form_data.get("protein"):
        return False, "Please choose one protein."
    else:
        return True, ""


def parse_multi_select(values):
    """Clean list values from checkboxes and remove empty items."""
    cleaned_values = []
    for value in values:
        text = value.strip()
        if text:
            cleaned_values.append(text)
    return cleaned_values


def format_currency(value):
    """Format float as USD text."""
    return f"${value:.2f}"


def format_list_for_display(text):
    """Format comma-separated string for display with fallback text."""
    cleaned = text.strip()
    if cleaned:
        return cleaned
    return "None"


def get_menu_options(category):
    """Return menu lists based on selected category."""
    toppings = ["Lettuce", "Tomato", "Onion", "Pickles", "Banana Peppers"]
    dressings = ["Mayo", "Ranch", "Chipotle", "Italian"]
    addons = ["Bacon", "Avocado", "Extra Cheese"]

    if category == "Sandwich":
        size_options = ["Small", "Large"]
        bread_or_tortilla_options = ["White Bread", "Wheat Bread", "Sourdough"]
    else:
        size_options = ["Regular"]
        bread_or_tortilla_options = ["Flour Tortilla", "Wheat Tortilla", "Spinach Tortilla"]

    return {
        "size_options": size_options,
        "bread_or_tortilla_options": bread_or_tortilla_options,
        "protein_options": ["Turkey", "Ham", "Chicken", "Steak", "Veggie"],
        "cheese_options": ["American", "Swiss", "Cheddar", "Pepper Jack"],
        "toppings": toppings,
        "dressings": dressings,
        "addons": addons,
    }
