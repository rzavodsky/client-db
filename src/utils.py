import math
from sqlalchemy.orm.query import Query

def paginate_query(query: Query, offset: int, limit: int):
    total_rows = query.count()
    total_pages = math.ceil(total_rows / limit)
    page_data = query.offset(offset).limit(limit).all()
    page_count = len(page_data)
    next_page = True if offset + page_count < total_rows else False
    if next_page:
        next_offset = offset + page_count
    else:
        next_offset = None

    return {
        "data": [row.as_dict() for row in page_data],
        "metadata": {
            "total_rows": total_rows,
            "total_pages": total_pages,
            "page_size": page_count,
            "next_page": next_page,
            "next_skip": next_offset
        }
    }
