from typing import Optional, List, Dict, Any

DEFAULT_LIMIT = 10
MAX_LIMIT = 100


def normalize_pagination(limit: Optional[int], offset: Optional[int]):
    if limit is None:
        limit = DEFAULT_LIMIT
    if limit > MAX_LIMIT:
        limit = MAX_LIMIT
    if offset is None or offset < 0:
        offset = 0
    return limit, offset


def build_page_meta(limit: int, offset: int, count_in_page: int, has_more: bool):
    next_offset = offset + count_in_page if has_more else None
    prev_offset = offset - limit if offset - limit >= 0 else None
    return {
        "next": next_offset,
        "limit": limit,
        "previous": prev_offset
    }