from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserResponse
from app.dependencies.db import get_db
from app.services.auth_service import register_user, login_user


router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session= Depends(get_db)):
    try:
        return register_user(db, user.email, user.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(user: UserCreate, db: Session=Depends(get_db)):
    try:
        token = login_user(db,user.email, user.password)
        return {"access-token": token}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))