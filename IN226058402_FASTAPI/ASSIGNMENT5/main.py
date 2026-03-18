from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

# ------------------ DATA ------------------

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 49, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "Pen Set", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 4, "name": "USB Cable", "price": 199, "category": "Electronics", "in_stock": False},
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False}
]

orders = []

# ------------------ BASIC ------------------

@app.get("/")
def home():
    return {"message": "FastAPI Assignment Running 🚀"}

@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}

# ------------------ Q1 SEARCH ------------------

@app.get("/products/search")
def search_products(keyword: str):
    result = [p for p in products if keyword.lower() in p["name"].lower()]

    if not result:
        return {"message": "No products found"}

    return result

# ------------------ Q2 SORT ------------------

@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):

    if sort_by not in ["price", "name"]:
        return {"error": "Invalid sort_by field"}

    sorted_products = sorted(
        products,
        key=lambda p: p[sort_by],
        reverse=(order == "desc")
    )

    return sorted_products

# ------------------ Q3 PAGINATION ------------------

@app.get("/products/page")
def paginate_products(page: int = 1, limit: int = 2):

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total": len(products),
        "products": products[start:end]
    }

# ------------------ CREATE ORDER ------------------

class Order(BaseModel):
    customer_name: str
    product_id: int
    quantity: int

@app.post("/orders")
def create_order(order: Order):
    orders.append(order.dict())
    return {"message": "Order created", "order": order}

# ------------------ Q4 ORDER SEARCH ------------------

@app.get("/orders/search")
def search_orders(customer_name: str):

    result = [
        o for o in orders
        if customer_name.lower() in o["customer_name"].lower()
    ]

    if not result:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(result),
        "orders": result
    }

# ------------------ Q5 SORT BY CATEGORY ------------------

@app.get("/products/sort-by-category")
def sort_by_category():

    result = sorted(products, key=lambda p: (p["category"], p["price"]))

    return {
        "products": result,
        "total": len(result)
    }

# ------------------ Q6 BROWSE (COMBINED) ------------------

@app.get("/products/browse")
def browse_products(
    keyword: str = Query(None),
    sort_by: str = Query("price"),
    order: str = Query("asc"),
    page: int = Query(1),
    limit: int = Query(4),
):

    result = products

    # SEARCH
    if keyword:
        result = [p for p in result if keyword.lower() in p["name"].lower()]

    # SORT
    if sort_by in ["price", "name"]:
        result = sorted(result, key=lambda p: p[sort_by], reverse=(order == "desc"))

    # PAGINATION
    total = len(result)
    start = (page - 1) * limit
    paged = result[start:start + limit]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total,
        "total_pages": -(-total // limit),
        "products": paged
    }

# ------------------ BONUS ------------------

@app.get("/orders/page")
def orders_page(page: int = 1, limit: int = 3):

    start = (page - 1) * limit

    return {
        "page": page,
        "limit": limit,
        "total": len(orders),
        "total_pages": -(-len(orders) // limit),
        "orders": orders[start:start + limit]
    }
