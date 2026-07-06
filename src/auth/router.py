from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.auth.schemas import UserCreate, Token, UserLogin
from src.auth.service import get_password_hash, verify_password, create_access_token
from src.repositories.user_repository import UserRepository
from domains.user.model import User
from infrastructure.db.session import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=dict)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if UserRepository.username_exists(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        tenant_id=user_data.tenant_id
    )
    UserRepository.create(db, new_user)
    return {"message": "User registered successfully"}

@router.post("/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = UserRepository.get_by_username(db, user_login.username)
    if not user or not verify_password(user_login.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.username, "tenant_id": str(user.tenant_id), "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}
