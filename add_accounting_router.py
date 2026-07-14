from pathlib import Path

p = Path("src/main.py")
text = p.read_text(encoding="utf-8")

import_line = "from src.domains.accounting.router import router as accounting_router"

if import_line not in text:
    target = "from src.business_profile_router import router as business_profile_router"
    text = text.replace(
        target,
        target + "\n" + import_line
    )

include_line = "app.include_router(accounting_router)"

if include_line not in text:
    target = "app.include_router(business_profile_router)"
    text = text.replace(
        target,
        target + "\n" + include_line
    )

p.write_text(text, encoding="utf-8")
print("✅ Accounting Router Added")
