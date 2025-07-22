from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Venta, VentaItem, Producto
from pydantic import BaseModel
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ItemVenta(BaseModel):
    producto_id: int
    cantidad: int

class VentaSchema(BaseModel):
    items: List[ItemVenta]

@router.post("/")
def registrar_venta(venta: VentaSchema, db: Session = Depends(get_db)):
    total = 0
    for item in venta.items:
        producto = db.query(Producto).filter(Producto.id == item.producto_id).first()
        if not producto or producto.stock < item.cantidad:
            raise HTTPException(status_code=400, detail="Producto no disponible o stock insuficiente")
        total += producto.precio * item.cantidad
        producto.stock -= item.cantidad

    nueva_venta = Venta(total=total)
    db.add(nueva_venta)
    db.flush()  # para obtener el ID antes de commit

    for item in venta.items:
        producto = db.query(Producto).filter(Producto.id == item.producto_id).first()
        venta_item = VentaItem(
            venta_id=nueva_venta.id,
            producto_id=producto.id,
            cantidad=item.cantidad,
            precio_unitario=producto.precio
        )
        db.add(venta_item)

    db.commit()
    return {"venta_id": nueva_venta.id, "total": total}
