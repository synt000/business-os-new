from pathlib import Path

path = Path("src/main.py")
text = path.read_text()

text = text.replace(
    "from src.domains.social_center.router import router as social_router\n",
    ""
)

text = text.replace(
    "\napp.include_router(social_router)\n",
    "\n"
)

path.write_text(text)

print("✅ Done")
