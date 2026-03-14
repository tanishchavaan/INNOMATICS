from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# ------------------------
# Dummy product database
# ------------------------
products = {
    1: {"name": "Wireless Mouse", "price": 499, "in_stock": True},
    2: {"name": "Notebook", "price": 99, "in_stock": True},
    3: {"name": "USB Hub", "price": 799, "in_stock": False}
}

# ------------------------
# Cart + Orders storage
# ------------------------
cart = {}
orders = []

# ------------------------
# Checkout model
# ------------------------
class Checkout(BaseModel):
    customer_name: str
    delivery_address: str


# ------------------------
# Q1 + Q4 Add item to cart
# ------------------------
@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int = 1):

    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    product = products[product_id]

    if not product["in_stock"]:
        raise HTTPException(status_code=400, detail="Product out of stock")

    if product_id in cart:
        cart[product_id]["quantity"] += quantity
    else:
        cart[product_id] = {
            "name": product["name"],
            "price": product["price"],
            "quantity": quantity
        }

    subtotal = cart[product_id]["price"] * cart[product_id]["quantity"]

    return {
        "message": "Item added to cart",
        "product": product["name"],
        "quantity": cart[product_id]["quantity"],
        "subtotal": subtotal
    }


# ------------------------
# Q2 View cart
# ------------------------
@app.get("/cart")
def view_cart():

    items = []
    total = 0

    for pid, item in cart.items():
        subtotal = item["price"] * item["quantity"]
        total += subtotal

        items.append({
            "product_id": pid,
            "name": item["name"],
            "quantity": item["quantity"],
            "subtotal": subtotal
        })

    return {
        "items": items,
        "item_count": len(items),
        "grand_total": total
    }


# ------------------------
# Q5 Remove item
# ------------------------
@app.delete("/cart/{product_id}")
def remove_item(product_id: int):

    if product_id not in cart:
        raise HTTPException(status_code=404, detail="Item not in cart")

    removed = cart.pop(product_id)

    return {
        "message": f"{removed['name']} removed from cart"
    }


# ------------------------
# Q5 Checkout
# ------------------------
@app.post("/cart/checkout")
def checkout(order: Checkout):

    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total = 0
    items = []

    for item in cart.values():
        subtotal = item["price"] * item["quantity"]
        total += subtotal
        items.append(item)

    order_data = {
        "customer": order.customer_name,
        "address": order.delivery_address,
        "items": items,
        "total": total
    }

    orders.append(order_data)

    cart.clear()

    return {
        "message": "Order placed successfully",
        "order": order_data
    }


# ------------------------
# View all orders
# ------------------------
@app.get("/orders")
def get_orders():
    return {"orders": orders}
