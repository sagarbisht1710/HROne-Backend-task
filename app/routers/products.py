from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List, Any
from bson import ObjectId
from app.db.mongo import get_db
from app.schemas.product import ProductCreate
from app.models.product import PRODUCT_COLLECTION, product_to_list_item
from app.utils.pagination import normalize_pagination, build_page_meta

router = APIRouter(prefix="/products", tags=["products"])

@router.post("", status_code=201)
async def create_product(payload: ProductCreate, db = Depends(get_db)):
    # Enforce unique name (case-insensitive) for demonstration
    existing = await db[PRODUCT_COLLECTION].find_one({"name": {"$regex": f"^{payload.name}$", "$options": "i"}})
    if existing:
        raise HTTPException(status_code=400, detail="Product with this name already exists")
    doc = payload.model_dump()
    result = await db[PRODUCT_COLLECTION].insert_one(doc)
    return {"id": str(result.inserted_id)}

@router.get("")
async def list_products(
    name: Optional[str] = Query(None, description="Partial name or regex (case-insensitive)"),
    size: Optional[str] = Query(None, description="Filter products containing this size label"),
    limit: Optional[int] = Query(None, ge=1),
    offset: Optional[int] = Query(None, ge=0),
    db = Depends(get_db)
):
    limit, offset = normalize_pagination(limit, offset)
    filters: dict[str, Any] = {}
    if name:
        # Use case-insensitive regex; if user supplies raw regex it's accepted as substring matching
        filters["name"] = {"$regex": name, "$options": "i"}
    if size:
        filters["sizes.size"] = {"$regex": f"^{size}$", "$options": "i"}

    cursor = db[PRODUCT_COLLECTION].find(filters, projection={"sizes": 0}).sort("_id", 1).skip(offset).limit(limit + 1)
    docs: List[dict] = await cursor.to_list(length=limit + 1)

    has_more = len(docs) > limit
    docs_page = docs[:limit]
    data = [product_to_list_item(d) for d in docs_page]

    page = build_page_meta(limit, offset, len(docs_page), has_more)
    return {"data": data, "page": page}