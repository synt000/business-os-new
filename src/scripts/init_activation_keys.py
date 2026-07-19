from src.core.database import engine, Base

# Load models
from src.domains.subscription.models import ActivationKey


def init():
    Base.metadata.create_all(bind=engine)
    print("ACTIVATION KEY TABLE READY")


if __name__ == "__main__":
    init()
