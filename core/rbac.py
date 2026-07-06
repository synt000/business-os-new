from fastapi import HTTPException, Depends
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi.security import OAuth2PasswordBearer
from core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


class RoleChecker:

    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def __call__(self, token: str = Depends(oauth2_scheme)):

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

            role = payload.get("role")

            if role not in self.allowed_roles:
                raise HTTPException(status_code=403, detail="Forbidden")

            return payload

        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
