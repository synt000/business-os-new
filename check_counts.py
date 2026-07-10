from src.core.database import SessionLocal
from src.models.saas_core import Product, Order, Customer, Supplier

db = SessionLocal()

print("Products :", db.query(Product).count())
print("Orders   :", db.query(Order).count())
print("Customers:", db.query(Customer).count())
print("Suppliers:", db.query(Supplier).count())
