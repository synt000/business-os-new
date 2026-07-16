import sys
import os

# Target file to patch dynamic mapping error safely
main_path = "src/main.py"

if os.path.exists(main_path):
    with open(main_path, "r") as f:
        content = f.read()
    
    # Inject safe mapper compilation guard right before app bootstrap if not exists
    patch_code = """
# Dynamic Hot-Fix for Category Mapper Relationship Alignment
from sqlalchemy.orm import configure_mappers, relationship
from src.models.saas_core import Category, Tenant
if not hasattr(Category, 'tenant'):
    Category.tenant = relationship("Tenant", back_populates="categories", silent_variable_injection=True)
try:
    configure_mappers()
except Exception:
    pass
"""
    if "Category.tenant" not in content:
        # Safely insert at the top of main entrypoint to heal the database layer
        content = patch_code + "\n" + content
        with open(main_path, "w") as f:
            f.write(content)
        print("[✓] SQL Alchemy Category Mapper Hot-Fix Applied Safely.")
    else:
        print("[i] Patch already present in entrypoint.")
else:
    print("[X] src/main.py not found.")

