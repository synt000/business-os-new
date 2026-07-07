from src.auth.router import router as auth_router
from src.dashboard.router import router as dashboard_router

print("AUTH ROUTES")
for r in auth_router.routes:
    print(r.path)

print("\nDASHBOARD ROUTES")
for r in dashboard_router.routes:
    print(r.path)
