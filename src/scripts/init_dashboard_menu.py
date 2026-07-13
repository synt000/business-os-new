from src.core.database import Base, engine
from src.models.saas_core import DashboardMenu

print("=== DASHBOARD MENU INIT ===")

Base.metadata.create_all(bind=engine)

print("✓ Dashboard Menu Created")
