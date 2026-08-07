from pathlib import Path

p = Path("src/main.py")
s = p.read_text()

old = """app.include_router(
    dashboard_router,
    prefix="/api/v4"
)
"""

if old not in s:
    print("TARGET NOT FOUND")
else:
    s = s.replace(old, "", 1)
    p.write_text(s)
    print("REMOVED dashboard_router include")
