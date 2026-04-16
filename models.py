"""Data models for Bistro Burnett.

Includes the Order class required by the assignment rubric.
"""


class Order:
    """Simple class representing a single Bistro Burnett order."""

    def __init__(
        self,
        phone_number,
        customer_name,
        category,
        size,
        bread_or_tortilla,
        protein,
        cheese="",
        toppings=None,
        dressings=None,
        addons=None,
        status="Received",
    ):
        self.phone_number = phone_number
        self.customer_name = customer_name
        self.category = category
        self.size = size
        self.bread_or_tortilla = bread_or_tortilla
        self.protein = protein
        self.cheese = cheese
        self.toppings = toppings if toppings is not None else []
        self.dressings = dressings if dressings is not None else []
        self.addons = addons if addons is not None else []
        self.status = status

    def calculate_total(self):
        """Calculate and return total order price.

        Pricing rules are intentionally simple for a classroom prototype.
        """
        total_price = 0.0

        if self.category == "Sandwich":
            if self.size == "Small":
                total_price = 7.99
            elif self.size == "Large":
                total_price = 10.99
            else:
                total_price = 0.0
        elif self.category == "Wrap":
            total_price = 8.99
        else:
            total_price = 0.0

        # Optional add-on charges.
        total_price += len(self.addons) * 0.75

        # Optional protein premium examples.
        if self.protein == "Steak":
            total_price += 1.50
        elif self.protein == "Chicken":
            total_price += 1.00

        return round(total_price, 2)

    def format_summary(self):
        """Return a formatted text summary of this order."""
        toppings_text = ", ".join(self.toppings) if self.toppings else "None"
        dressings_text = ", ".join(self.dressings) if self.dressings else "None"
        addons_text = ", ".join(self.addons) if self.addons else "None"
        cheese_text = self.cheese if self.cheese else "None"

        summary_lines = [
            f"Category: {self.category}",
            f"Size: {self.size}",
            f"Bread/Tortilla: {self.bread_or_tortilla}",
            f"Protein: {self.protein}",
            f"Cheese: {cheese_text}",
            f"Toppings: {toppings_text}",
            f"Dressings: {dressings_text}",
            f"Add-ons: {addons_text}",
            f"Total: ${self.calculate_total():.2f}",
        ]
        return " | ".join(summary_lines)
