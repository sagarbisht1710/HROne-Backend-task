from typing import Any, Dict

ORDER_COLLECTION = "orders"

def order_to_public(doc: Dict[str, Any]) -> Dict[str, Any]:
    # Items already enriched upstream
    return {
        "id": str(doc["_id"]),
        "userId": doc["userId"],
        "items": doc["items"],
        "total": doc["total"],
        "createdAt": doc.get("createdAt")
    }