from fastapi import Depends, HTTPException, status
from datetime import timedelta
from dotenv import load_dotenv
import os
from utilities.crypt import create_access_token, decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer(auto_error=False)

load_dotenv()

MASTERADMIN_USERNAME = os.getenv("MASTERADMIN_USERNAME")
MASTERADMIN_PASSWORD = os.getenv("MASTERADMIN_PASSWORD")

def authenticate_user(username: str, password: str):
    return username == MASTERADMIN_USERNAME and password == MASTERADMIN_PASSWORD

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    if credentials is None:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_token(credentials.credentials)
    if not payload or payload.get("sub") != MASTERADMIN_USERNAME:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": MASTERADMIN_USERNAME, "role": "masteradmin"}
