from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException
from core.config import settings
from repositories.user_repository import UserRepository
from core.security import hash_password, verify_password

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


class AuthService:

    @staticmethod
    def register(db, username: str, password: str, role: str, tenant_id: str):
        hashed = hash_password(password)

        user = UserRepository.create_user(
            db=db,
            username=username,
            password_hash=hashed,
            role=role,
            tenant_id=tenant_id
        )

        return {"message": "User created"}

    @staticmethod
    def login(db, username: str, password: str):
        user = UserRepository.get_by_username(db, username)

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        expire = datetime.utcnow() + timedelta(minutes=EXPIRE_MINUTES)

        token = jwt.encode(
            {
                "sub": str(user.id),
                "role": user.role,
                "tenant_id": str(user.tenant_id),
                "exp": expire  # 🔥 CRITICAL SECURITY FIX
            },
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return {"access_token": token, "token_type": "bearer"}
