from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Producto
from pydantic import BaseModel
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ProductoSchema(BaseModel):
    nombre: str
    precio: float
    stock: int

class ProductoOut(ProductoSchema):
    id: int
    class Config:
        orm_mode = True

@router.post("/", response_model=ProductoOut)
def crear_producto(producto: ProductoSchema, db: Session = Depends(get_db)):
    db_producto = Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.get("/", response_model=List[ProductoOut])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()
