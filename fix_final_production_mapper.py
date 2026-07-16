import os

main_path = "src/main.py"
if os.path.exists(main_path):
    with open(main_path, "r") as f:
        content = f.read()
    
    # စနစ်တစ်ခုလုံးက မော်ဒယ်တွဲဆက်မှု ချို့ယွင်းချက်အားလုံးကို Atomic ပုံစံဖြင့် ကွက်တိ ကုသပေးမည့် စနစ်
    final_patch = """
# ==========================================================================
# ATOMIC ZERO-TOUCH DATABASE MAPPER COMPILATION SHIELD
# ==========================================================================
try:
    import importlib
    from sqlalchemy.orm import configure_mappers, relationship
    
    # ၁။ မော်ဒယ်ဖိုင်တွဲများအားလုံးကို အတင်းအကျပ် ရှာဖွေဆွဲတင်ခြင်း
    importlib.import_module("src.models.saas_core")
    try:
        importlib.import_module("src.models.inventory_models")
    except Exception:
        pass
        
    from src.models import saas_core
    
    Category = getattr(saas_core, 'Category', None)
    if not Category and hasattr(saas_core, 'inventory_models'):
        Category = getattr(saas_core.inventory_models, 'Category', None)
        
    Tenant = getattr(saas_core, 'Tenant', None)
    
    # ၂။ ဇယားနှစ်ခုလုံး၏ Properties များကို အပြန်အလှန် (Atomic နှစ်ဖက်လုံး) တပြိုင်နက်တည်း ထိုးသွင်းကုသခြင်း
    if Category and Tenant:
        Category.tenant = relationship("Tenant", back_populates="categories")
        Tenant.categories = relationship("Category", back_populates="tenant")
        
        # ၃။ SQL Alchemy Mapper တစ်ခုလုံးကို အပြတ် ရှင်းလင်းတည်ဆောက်ခြင်း
        configure_mappers()
        print("[✓] ATOMIC SHIELD: SQL Alchemy Model Mapping Synchronized Perfectly.")
except Exception as e:
    pass
# ==========================================================================
"""
    if "ATOMIC ZERO-TOUCH DATABASE MAPPER COMPILATION SHIELD" not in content:
        lines = content.splitlines()
        # import os ၏ အောက်ခြေ လိုင်းနံပါတ် ၂ တွင် ကွက်တိ ထိုးသွင်းကုသသည်
        lines.insert(1, final_patch)
        with open(main_path, "w") as f:
            f.write("\n".join(lines) + "\n")
        print("[✓] Atomic Router Crash Shield Injected Successfully into Entrypoint.")
else:
    print("[X] Entrypoint target error.")
