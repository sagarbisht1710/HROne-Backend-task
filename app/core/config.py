from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    MONGO_URl: str = os.getenv("MONGO_URl", "mongodb://localhost:27017")
    MONGO_DB: str = os.getenv("MONGO_DB", "ecommerce_db")
    APP_NAME: str = os.getenv("APP_NAME", "FastAPI ECommerce")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0")

settings = Settings()
