from pathlib import Path

file = Path("src/auth/router.py")

text = file.read_text()

text = text.replace(
    "register_failed_login(user, db)",
    "register_failed_login(db, user)"
)

text = text.replace(
    "register_success_login(user, db)",
    "register_success_login(db, user)"
)

file.write_text(text)

print("LOGIN GUARD CALLS PATCHED")
