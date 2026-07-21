from pathlib import Path

p = Path("src/domains/dashboard/router.py")

text = p.read_text()

old = """router = APIRouter(
    tags=["Owner Dashboard"]
)"""

new = """router = APIRouter(
    prefix="/owner",
    tags=["Owner Dashboard"]
)"""

if old in text:
    text=text.replace(old,new,1)
    p.write_text(text)
    print("✅ Restored owner prefix")
else:
    print("❌ Not found")
