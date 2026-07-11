from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    tenant_id: UUID

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    tenant_id: Optional[UUID] = None
    role: Optional[str] = None
