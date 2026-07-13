from src.core.database import Base, engine
from src.models.saas_core import (
    AIBusinessMemory,
    AIConversation,
    AIInsight,
)

print("=== AI TABLE INIT ===")

Base.metadata.create_all(bind=engine)

print("✓ AI Tables Created")
