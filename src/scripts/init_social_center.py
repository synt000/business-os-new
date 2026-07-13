from src.core.database import Base, engine

from src.models.saas_core import (
    BusinessProfile,
    SocialAccount
)


print("=== SOCIAL CENTER INIT ===")


Base.metadata.create_all(
    bind=engine
)


print("✓ Business Profile")
print("✓ Social Account")
