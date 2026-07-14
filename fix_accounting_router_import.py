from pathlib import Path

p = Path("src/domains/accounting/router.py")
text = p.read_text(encoding="utf-8")

text = text.replace(
    "from src.auth.dependencies import get_current_user",
    "from src.core.security import get_current_user"
)

p.write_text(text, encoding="utf-8")
print("✅ Accounting router import fixed")
