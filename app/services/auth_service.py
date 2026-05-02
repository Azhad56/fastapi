from sqlalchemy.orm import Session
from app.repositories.user_repo import get_user_by_email, create_user
from app.core.security import hash_password
from app.core.security import verify_password, create_access_token, decode_access_token
from app.dependencies.auth import oauth2_scheme
from fastapi import Depends, HTTPException,status
from app.dependencies.db import get_db

def register_user(db: Session, email: str, password: str):

    existing_user = get_user_by_email(db, email)

    if existing_user:
        raise Exception("User already exists")
    
    hashed_password = hash_password(password)

    return create_user(db, email, hashed_password)

def login_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user or not verify_password(password, user.password):
        raise Exception("Invalid credentials")
    
    token = create_access_token({ "sub": user.email })
    return token


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token"
        )
    email = payload.get("sub")

    if email is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token payload"
        )
    
    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not found"
        )
    
    return user