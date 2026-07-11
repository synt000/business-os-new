from sqlalchemy import text
from src.core.database import engine

columns = [
    ("two_factor_enabled", "BOOLEAN DEFAULT 0"),
    ("two_factor_secret", "VARCHAR"),
    ("backup_codes", "TEXT")
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
            print("SKIP:", name)

    conn.commit()

print("2FA MIGRATION COMPLETE")
