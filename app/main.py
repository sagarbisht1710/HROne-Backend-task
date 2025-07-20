from fastapi import FastAPI
from app.core.config import settings
from app.routers import products, orders

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

@app.get("/")
async def root():
    return {"message": "E-Commerce API running", "version": settings.APP_VERSION}

app.include_router(products.router)
app.include_router(orders.router)