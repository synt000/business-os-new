"""
Order domain models are centralized in saas_core.
This file keeps compatibility imports.
"""

from src.models.saas_core import (
    Order,
    OrderItem
)

__all__ = [
    "Order",
    "OrderItem"
]
