from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    precio = Column(Float)
    stock = Column(Integer)

class Venta(Base):
    __tablename__ = "ventas"
    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    total = Column(Float)

class VentaItem(Base):
    __tablename__ = "venta_items"
    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer)
    precio_unitario = Column(Float)
