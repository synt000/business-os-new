from src.core.database import engine, Base

# Load models
from src.models.saas_core import *
from src.models.subscription import *

print("Creating subscription tables...")

Base.metadata.create_all(bind=engine)

print("SUBSCRIPTION TABLES CREATED")
