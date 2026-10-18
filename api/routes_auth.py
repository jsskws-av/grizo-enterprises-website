"""
Authentication and Session Routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
import hashlib

from database.connection import get_sync_db
from database.models import User
from database.seed_data import hash_password

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    username: str
    role: str
    token: str


@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest):
    db = get_sync_db()
    try:
        user = db.query(User).filter(User.username == req.username).first()
        if not user or user.hashed_password != hash_password(req.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
        
        # Simple token representation for SPA
        token = f"sess_{user.id}_{hashlib.sha256((user.username + 'salt').encode()).hexdigest()[:16]}"
        return LoginResponse(
            username=user.username,
            role=user.role,
            token=token
        )
    finally:
        db.close()


@router.get("/me")
def get_current_user():
    return {"username": "admin", "role": "admin", "authenticated": True}
