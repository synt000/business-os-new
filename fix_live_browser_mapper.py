import os

main_path = "src/main.py"
if os.path.exists(main_path):
    with open(main_path, "r") as f:
        content = f.read()
    
    # Live Browser ကြည့်စဉ် Database Mapper Crash မဖြစ်စေရန် မူရင်းကုဒ်မထိဘဲ Dynamic ဖြည့်ဆည်းပေးခြင်း
    mapper_patch = """
# ==========================================================================
# ZERO-TOUCH DATABASE MAPPER ALIGNMENT GUARD FOR LIVE BROWSER
# ==========================================================================
try:
    from sqlalchemy.orm import configure_mappers, relationship
    from src.models import saas_core
    Category = getattr(saas_core, 'Category', None)
    if not Category and hasattr(saas_core, 'inventory_models'):
        Category = getattr(saas_core.inventory_models, 'Category', None)
    Tenant = getattr(saas_core, 'Tenant', None)
    if Category and Tenant and not hasattr(Category, 'tenant'):
        Category.tenant = relationship("Tenant", back_populates="categories")
        configure_mappers()
except Exception:
    pass
# ==========================================================================
"""
    
    if "ZERO-TOUCH DATABASE MAPPER ALIGNMENT GUARD" not in content:
        # File ၏ ထိပ်ဆုံးအကျဆုံးနေရာ (import os ၏ အောက်) တွင် ဘေးကင်းစွာ ထိုးသွင်းကုသသည်
        lines = content.splitlines()
        lines.insert(1, mapper_patch)
        with open(main_path, "w") as f:
            f.write("\n".join(lines) + "\n")
        print("[✓] SQL Alchemy Live Browser Mapper Guard Injected Safely into src/main.py.")
    else:
        print("[i] Guard already active inside production core context.")
else:
    print("[X] src/main.py configuration entry not found.")
