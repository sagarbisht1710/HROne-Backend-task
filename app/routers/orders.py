from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List, Dict, Any
from bson import ObjectId
from datetime import datetime
from app.db.mongo import get_db
from app.schemas.order import OrderCreate
from app.models.product import PRODUCT_COLLECTION, total_available_quantity, deduct_inventory
from app.models.order import ORDER_COLLECTION
from app.utils.pagination import normalize_pagination, build_page_meta

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("", status_code=201)
async def create_order(payload: OrderCreate, db = Depends(get_db)):
    # Fetch all products referenced (deduplicate first)
    product_ids = list({item.productId for item in payload.items})
    obj_ids = []
    for pid in product_ids:
        try:
            obj_ids.append(ObjectId(pid))
        except Exception:
            raise HTTPException(status_code=400, detail=f"Invalid productId format: {pid}")

    products_map: Dict[str, Dict[str, Any]] = {}
    async for p in db[PRODUCT_COLLECTION].find({"_id": {"$in": obj_ids}}):
        products_map[str(p["_id"])] = p

    # Validate existence
    for item in payload.items:
        if item.productId not in products_map:
            raise HTTPException(status_code=404, detail=f"Product not found: {item.productId}")

    # Validate stock and build price map
    for item in payload.items:
        prod = products_map[item.productId]
        available = total_available_quantity(prod)
        if available < item.qty:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for product {item.productId}")

    # Deduct inventory (mutate in-place) & compute totals
    order_items = []
    order_total = 0.0
    for item in payload.items:
        prod = products_map[item.productId]
        # Deduct
        deduct_inventory(prod, item.qty)
        # Persist updated product inventory
        await db[PRODUCT_COLLECTION].update_one(
            {"_id": prod["_id"]}, {"$set": {"sizes": prod.get("sizes", [])}}
        )
        # Need product price
        price = prod["price"]
        line_total = price * item.qty
        order_total += line_total
        order_items.append({
            "productId": item.productId,
            "qty": item.qty,
            # Defer productDetails enrichment to listing endpoint only
        })

    order_doc = {
        "userId": payload.userId,
        "items": order_items,
        "total": order_total,
        "createdAt": datetime.utcnow()
    }
    result = await db[ORDER_COLLECTION].insert_one(order_doc)
    return {"id": str(result.inserted_id)}

@router.get("/{user_id}")
async def list_orders_for_user(
    user_id: str,
    limit: Optional[int] = Query(None, ge=1),
    offset: Optional[int] = Query(None, ge=0),
    db = Depends(get_db)
):
    limit, offset = normalize_pagination(limit, offset)

    cursor = db[ORDER_COLLECTION].find({"userId": user_id}).sort("_id", 1).skip(offset).limit(limit + 1)
    docs = await cursor.to_list(length=limit + 1)
    has_more = len(docs) > limit
    docs_page = docs[:limit]

    # Collect all productIds to batch fetch
    all_product_ids = set()
    for d in docs_page:
        for it in d.get("items", []):
            all_product_ids.add(it["productId"])
    obj_ids = []
    for pid in all_product_ids:
        try:
            obj_ids.append(ObjectId(pid))
        except Exception:
            continue

    products_map: Dict[str, Dict[str, Any]] = {}
    if obj_ids:
        async for p in db[PRODUCT_COLLECTION].find({"_id": {"$in": obj_ids}}):
            products_map[str(p["_id"])] = p

    response_orders = []
    for d in docs_page:
        enriched_items = []
        for it in d.get("items", []):
            prod = products_map.get(it["productId"])  # Product may be missing if deleted
            if prod:
                prod_details = {
                    "id": str(prod["_id"]),
                    "name": prod["name"],
                    "price": prod["price"],
                }
                line_total = prod["price"] * it["qty"]
            else:
                prod_details = None
                line_total = 0
            enriched_items.append({
                "productId": it["productId"],
                "qty": it["qty"],
                "productDetails": prod_details,
                "lineTotal": line_total
            })
        total = sum(i["lineTotal"] for i in enriched_items)
        response_orders.append({
            "id": str(d["_id"]),
            "items": enriched_items,
            "total": total
        })

    page = build_page_meta(limit, offset, len(docs_page), has_more)
    return {"data": response_orders, "page": page}