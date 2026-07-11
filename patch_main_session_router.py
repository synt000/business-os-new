from pathlib import Path

p = Path("src/main.py")
text = p.read_text()

if "from src.auth.session_router import router as session_router" not in text:
    text = text.replace(
        "from src.auth.two_factor import router as two_factor_router",
        "from src.auth.two_factor import router as two_factor_router\nfrom src.auth.session_router import router as session_router"
    )

if "app.include_router(session_router)" not in text:
    text = text.replace(
        "app.include_router(two_factor_router)",
        "app.include_router(two_factor_router)\napp.include_router(session_router)"
    )

p.write_text(text)

print("SESSION ROUTER REGISTERED")
