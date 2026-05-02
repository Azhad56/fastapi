from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.db.base import Base
from app.db.session import engine
from app.models import user
from app.routes import auth,user

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-commerce API",
    version="1.0.0",
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(user.router, prefix="/user", tags=["Users"])

@app.get("/")
def health_check() -> dict:
    return {"status": "OK"}

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return { "message": "Db connected successfully" }