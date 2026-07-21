from pathlib import Path

p = Path("src/main.py")

s = p.read_text()

if "from src.domains.accounting.router import router as accounting_router" not in s:
    s = s.replace(
        "from src.domains.finance.router import router as finance_router",
        "from src.domains.finance.router import router as finance_router\nfrom src.domains.accounting.router import router as accounting_router"
    )

if "app.include_router(accounting_router)" not in s:
    s = s.replace(
        "app.include_router(finance_router)",
        "app.include_router(finance_router)\napp.include_router(accounting_router)"
    )

p.write_text(s)

print("Accounting router added")
