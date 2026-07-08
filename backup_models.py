from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, default="user")
    # ဒီမှာ password_hash ကို သေချာထည့်ပေးပါ
    password_hash = Column(String, nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
