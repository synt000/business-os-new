from pathlib import Path

file = Path("src/main.py")
text = file.read_text()

if "from src.auth.refresh_router import router as refresh_router" not in text:
    text = text.replace(
        "from src.auth.session_router import router as session_router",
        "from src.auth.session_router import router as session_router\n"
        "from src.auth.refresh_router import router as refresh_router"
    )

if "app.include_router(refresh_router)" not in text:
    pos = text.find("app.include_router(session_router)")
    if pos != -1:
        end = text.find("\n", pos)
        text = (
            text[:end + 1]
            + "app.include_router(refresh_router)\n"
            + text[end + 1:]
        )

file.write_text(text)
print("REFRESH ROUTER REGISTERED")
