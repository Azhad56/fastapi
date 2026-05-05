from fastapi import APIRouter , HTTPException, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.services.auth_service import get_current_user
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import createNewProduct , removeProduct , list_products

router = APIRouter()

#public route 

@router.get("/", response_model=list[ProductResponse])
def products(db: Session = Depends(get_db)):
    return list_products(db)

# Authenticated Route - create product

@router.post("/", response_model=ProductResponse)
def create_product(data: ProductCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    return createNewProduct(db, data, user)

# Authenticated and authorised route - delete product
@router.delete("/{product_id}")
def delete_product_route(product_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        removeProduct(db, product_id, user)
        return {"message": "Product deleted"}
    except Exception as e:
        raise HTTPException(status_code=403 , detail=str(e))