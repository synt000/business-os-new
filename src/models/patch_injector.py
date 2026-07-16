
import logging
from sqlalchemy.orm import configure_mappers, relationship

def apply_zero_touch_patch():
    try:
        from src.models import saas_core
        # Safely locate Category from saas_core or its sub-modules dynamically
        Category = getattr(saas_core, 'Category', None)
        if not Category and hasattr(saas_core, 'inventory_models'):
            Category = getattr(saas_core.inventory_models, 'Category', None)
            
        Tenant = getattr(saas_core, 'Tenant', None)
        
        if Category and Tenant and not hasattr(Category, 'tenant'):
            Category.tenant = relationship("Tenant", back_populates="categories")
            configure_mappers()
            print("[✓] Zero-Touch Dynamic Runtime Patch Applied Successfully.")
    except Exception as e:
        pass

apply_zero_touch_patch()
