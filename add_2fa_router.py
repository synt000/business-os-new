from pathlib import Path

p = Path("src/main.py")

text = p.read_text()

if "from src.auth.two_factor import router as two_factor_router" not in text:

    text = text.replace(
        "from src.auth.router import router as auth_router",
        "from src.auth.router import router as auth_router\nfrom src.auth.two_factor import router as two_factor_router"
    )


if "app.include_router(two_factor_router)" not in text:

    text = text.replace(
        "app.include_router(auth_router)",
        "app.include_router(auth_router)\napp.include_router(two_factor_router)"
    )


p.write_text(text)

print("2FA ROUTER ADDED")
