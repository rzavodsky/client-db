import math
from sqlalchemy.orm.query import Query
from app import db

def paginate_query(query: Query, offset: int, limit: int) -> dict:
    """Returns paginated data from database along with some metadata"""
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

def autoincrement_id(context):
    """Increments a number in the top_ids table based on the table name and returns the incremented number
    This function should be used as the default for all id columns instead of autoincrement"""
    table_name = context.current_column.table.name
    db.session.execute("UPDATE Top_IDs SET top_ID = top_ID + 1 WHERE top_table = :table_name", {"table_name": table_name})
    result = db.session.execute(
        "SELECT top_ID FROM Top_IDs WHERE top_table = :table_name",
        {"table_name": table_name}).scalar()
    return result
