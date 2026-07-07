import src.main

print("Main file:", src.main.__file__)
print()

print("Dashboard router:")
print(src.main.dashboard_router)

print()
print("App routes:")
for r in src.main.app.routes:
    print(type(r).__name__, getattr(r, "path", None))
