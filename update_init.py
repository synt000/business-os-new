from pathlib import Path

p = Path("src/telegram_bot/keyboards/__init__.py")
s = p.read_text()

adds = [
    "from .dashboard import dashboard_menu",
    "from .users_center import users_center_menu",
    "from .settings import settings_menu",
]

for a in adds:
    if a not in s:
        s = s.replace(
            "from .ceo import ceo_main_menu",
            "from .ceo import ceo_main_menu\n" + a
        )

for n in [
    '"dashboard_menu"',
    '"users_center_menu"',
    '"settings_menu"',
]:
    if n not in s:
        s = s.replace(
            "__all__ = [",
            "__all__ = [\n    " + n + ","
        )

p.write_text(s)

print("✅ keyboard exports updated")
