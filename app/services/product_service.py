from sqlalchemy.orm import Session
from app.repositories.product_repo import  create, get_all_products , product_by_id , delete

def createNewProduct (db: Session, data, user):
    return create(db, data, user.id)

def list_products(db: Session):
    return get_all_products(db)

def removeProduct(db: Session, product_id: int, user):
    product = product_by_id(db, product_id)
    if not product:
        raise Exception("Product not found")
    #Authorisation check
    if user.role != "admin" and product.owner_id != user.id:
        raise Exception("Not authorised to delete the product")
    
    delete(db, product)
    return True
