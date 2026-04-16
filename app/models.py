"""
Title: Bistro Burnett Models
Author: Team 015-4
Date: April 16, 2026
Purpose: Defines the Order class to manage food data and logic.
"""

class Order:
    """Represents a customer's food order[cite: 73]."""
    
    def __init__(self, category, size, protein):
        self.category = category
        self.size = size
        self.protein = protein
        self.base_price = 0.0

    def calculate_total(self, addon_count):
        """
        Purpose: Calculates the total price[cite: 73].
        Input: addon_count (int)
        Output: total_price (float)
        """
        # Decision structure (if/elif/else) 
        if self.category == "Sandwich":
            if self.size == "12 inch":
                self.base_price = 10.99
            else:
                self.base_price = 7.99
        else:
            self.base_price = 8.99 # Wraps are flat rate
            
        # Add-ons cost extra [cite: 261]
        total = self.base_price + (addon_count * 1.50)
        return round(total, 2)
