from fastapi import FastAPI
from app.core.config import settings
from app.routers import products, orders
import os
import motor.motor_asyncio
MONGO_URI = os.environ.get("MONGO_URl")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.get_database()  # default DB from URI
app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)

@app.get("/")
async def root():
    return {"message": "E-Commerce API running", "version": settings.APP_VERSION}

app.include_router(products.router)
app.include_router(orders.router)
