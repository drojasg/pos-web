from fastapi import FastAPI
from routers import productos, ventas
from database import Base, engine

# Crear las tablas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Incluir rutas
app.include_router(productos.router, prefix="/productos", tags=["Productos"])
app.include_router(ventas.router, prefix="/ventas", tags=["Ventas"])
