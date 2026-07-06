from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import List
import sqlite3

app = FastAPI(title="Business OS API")

SECRET_KEY = "SUPER_SECRET_KEY_REPLACE_IN_PROD"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    conn = sqlite3.connect("business_os.db")
    conn.row_factory = sqlite3.Row
    return conn

# Role Checker
class RoleChecker:
    def __init__(self, allowed_roles: List[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            role = payload.get("role")
            if role not in self.allowed_roles:
                raise HTTPException(status_code=403, detail="Operation not permitted")
            return payload
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

@app.on_event("startup")
async def startup():
    conn = get_db()
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, hashed_password TEXT, role TEXT)")
    conn.commit()
    conn.close()

@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...), role: str = Form("staff")):
    conn = get_db()
    try:
        conn.execute("INSERT INTO users (username, hashed_password, role) VALUES (?, ?, ?)", 
                     (username, pwd_context.hash(password), role))
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")
    finally:
        conn.close()
    return {"message": "User created"}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_db()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (form_data.username,)).fetchone()
    conn.close()
    if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode({"sub": user["username"], "role": user["role"]}, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/admin-only", dependencies=[Depends(RoleChecker(["admin"]))])
async def admin_only():
    return {"message": "Hello Admin!"}
