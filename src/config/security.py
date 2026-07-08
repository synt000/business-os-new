import os
from datetime import datetime,timedelta,timezone
from typing import Optional
from jose import JWTError,jwt
from passlib.context import CryptContext
PWD_CONTEXT=CryptContext(schemes=["bcrypt"],deprecated="auto")
SECRET_KEY=os.getenv("SECRET_KEY","prod-business-os-enterprise-9.9-jwt-key-2026")
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
def get_password_hash(password:str)->str: return PWD_CONTEXT.hash(password)
def verify_password(plain_password:str,hashed_password:str)->bool: return PWD_CONTEXT.verify(plain_password,hashed_password)
def create_access_token(data:dict,expires_delta:Optional[timedelta]=None)->str:
 to_encode=data.copy(); expire=datetime.now(timezone.utc)+(expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)); to_encode.update({"exp":expire}); return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
def create_refresh_token(data:dict)->str:
 to_encode=data.copy(); expire=datetime.now(timezone.utc)+timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS); to_encode.update({"exp":expire,"token_type":"refresh"}); return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
def verify_access_token(token:str)->Optional[dict]:
 try: return jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
 except JWTError: return None
