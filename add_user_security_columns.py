from sqlalchemy import text
from src.core.database import engine

columns = [
    ("failed_login_attempts", "INTEGER DEFAULT 0"),
    ("locked_until", "DATETIME"),
    ("last_login_at", "DATETIME")
]


with engine.connect() as conn:

    for name, dtype in columns:
        try:
            conn.execute(
                text(
                    f"ALTER TABLE users ADD COLUMN {name} {dtype}"
                )
            )
            print("ADDED:", name)

        except Exception as e:
            print("SKIP:", name, e)

    conn.commit()


print("USER SECURITY MIGRATION COMPLETE")
