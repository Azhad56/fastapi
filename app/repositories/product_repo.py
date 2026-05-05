from sqlalchemy.orm import Session
from app.models.product import Product

def create(db: Session, data, owner_id: int):
    product = Product(**data.dict(), owner_id=owner_id)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_all_products(db: Session):
    return db.query(Product).all()

def product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def delete(db: Session, product):
    db.delete(product)
    db.commit()
