from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 49, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "Pen Set", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 4, "name": "USB Cable", "price": 199, "category": "Electronics", "in_stock": False},
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False}
]

# Q1
@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }

# Q2
@app.get("/products/category/{category_name}")
def get_by_category(category_name: str):
    filtered = [p for p in products if p["category"].lower() == category_name.lower()]
    return {"category": category_name, "products": filtered}

# Q3
@app.get("/products/instock")
def instock_products():
    filtered = [p for p in products if p["in_stock"]]
    return {"instock_products": filtered}

# Q4
@app.get("/store/summary")
def store_summary():
    total_products = len(products)
    total_value = sum(p["price"] for p in products)
    return {
        "total_products": total_products,
        "total_store_value": total_value
    }

# Q5
@app.get("/products/search/{keyword}")
def search_products(keyword: str):
    result = [p for p in products if keyword.lower() in p["name"].lower()]
    return {"results": result}

# BONUS
@app.get("/products/deals")
def deals():
    result = [p for p in products if p["price"] < 500 and p["in_stock"]]
    return {"deals": result}
