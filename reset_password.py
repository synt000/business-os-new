from src.core.security import get_password_hash
import sqlite3

h = get_password_hash("123456")

db = sqlite3.connect("business.db")

db.execute(
    "UPDATE users SET hashed_password=? WHERE email=?",
    (h, "owner@demo.com")
)

db.commit()

print(
    db.execute(
        "SELECT hashed_password FROM users WHERE email=?",
        ("owner@demo.com",)
    ).fetchone()[0]
)

db.close()
