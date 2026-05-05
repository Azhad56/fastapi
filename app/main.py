from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.db.base import Base
from app.db.session import engine
from app.models import user,product
from app.routes import auth,user as userRoute, product as productRoute

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-commerce API",
    version="1.0.0",
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(userRoute.router, prefix="/user", tags=["Users"])
app.include_router(productRoute.router, prefix='/product', tags=["Product"])

@app.get("/")
def health_check() -> dict:
    return {"status": "OK"}

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return { "message": "Db connected successfully" }