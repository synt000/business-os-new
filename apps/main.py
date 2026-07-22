"""
Business OS Application Entry Point

Production entry delegates to src.main:
- Auth
- Orders
- Products
- Inventory
- Accounting
- SaaS modules
"""

from src.main import app
