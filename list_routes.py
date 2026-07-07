from src.main import app
from starlette.routing import Route, Mount

print("=" * 60)

for route in app.routes:
    if isinstance(route, Route):
        methods = ",".join(sorted(route.methods))
        print(f"{methods:20} {route.path}")
    elif isinstance(route, Mount):
        print(f"{'MOUNT':20} {route.path}")

print("=" * 60)
