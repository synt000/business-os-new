from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import sqlite3

app = FastAPI(title="Business OS API")

# Security Configs
SECRET_KEY = "SUPER_SECRET_KEY_REPLACE_IN_PROD"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# DB Helper
def get_db():
    conn = sqlite3.connect("business_os.db")
    return conn

# Password Hashing
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@app.on_event("startup")
async def startup():
    conn = get_db()
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, hashed_password TEXT, role TEXT)")
    conn.execute("CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, task TEXT, user_id INTEGER)")
    conn.close()

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Placeholder for authentication logic
    return {"access_token": "token", "token_type": "bearer"}

@app.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    return {"user": "current_user_data"}
