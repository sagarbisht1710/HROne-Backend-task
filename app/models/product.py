from typing import List, Dict, Any
from bson import ObjectId

PRODUCT_COLLECTION = "products"

# Helper conversions

def product_to_public(doc: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "price": doc["price"],
        "sizes": doc.get("sizes", [])
    }


def product_to_list_item(doc: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": str(doc["_id"]),
        "name": doc["name"],
        "price": doc["price"],
    }


def total_available_quantity(product: Dict[str, Any]) -> int:
    return sum(s.get("quantity", 0) for s in product.get("sizes", []))


def deduct_inventory(product: Dict[str, Any], qty: int) -> Dict[str, Any]:
    # Deduct from sizes in order until quantity satisfied
    remaining = qty
    for size_entry in product.get("sizes", []):
        if remaining <= 0:
            break
        available = size_entry.get("quantity", 0)
        if available <= 0:
            continue
        if available >= remaining:
            size_entry["quantity"] = available - remaining
            remaining = 0
        else:
            size_entry["quantity"] = 0
            remaining -= available
    if remaining > 0:
        raise ValueError("Not enough inventory after deduction logic (should not happen if pre-checked)")
    return product