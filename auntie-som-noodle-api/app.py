# app.py
# 🍜 Auntie Som’s Noodle Stall API
# Written lovingly by Nephew Lek (during school break)

from flask import Flask, request, jsonify
import uuid
import time

app = Flask(__name__)

# ----------------------
# In-memory data
# ----------------------
MENU = {
    1: {"name": "Tom Yum Noodles", "price": 50, "stock": 2},
    2: {"name": "Fried Rice", "price": 45, "stock": 1}
}

ORDERS = {}
TOKENS = {}

# ----------------------
# Authentication
# ----------------------


@app.post("/auth/login")
def login():
    data = request.json

    if data.get("username") == "student" and data.get("password") == "hungry":
        token = str(uuid.uuid4())

        TOKENS[token] = {
            "createdAt": time.time()
        }

        return jsonify({
            "accessToken": token,
            "expiresIn": 3600
        })

    return jsonify({"error": "Invalid login"}), 401


def require_auth():
    auth = request.headers.get("Authorization", "")
    token = auth.replace("Bearer ", "")

    if token in TOKENS:
        return True

    return False


# ----------------------
# Menu
# ----------------------
@app.get("/menu")
def get_menu():
    return jsonify([
        {"id": k, **v} for k, v in MENU.items()
    ])


# ----------------------
# Orders
# ----------------------
@app.post("/orders")
def create_order():
    if not require_auth():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    item_id = data.get("itemId")
    quantity = data.get("quantity")

    item = MENU.get(item_id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    if item["stock"] <= 0:
        return jsonify({"error": "Out of stock"}), 400

    item["stock"] -= quantity  # stock can go negative

    order_id = f"ORD-{uuid.uuid4().hex[:6]}"

    total_price = (item["price"] * quantity) - 5

    ORDERS[order_id] = {
        "status": "created",
        "totalPrice": total_price
    }

    return jsonify({
        "orderId": order_id,
        "status": "created",
        "totalPrice": total_price
    })


# ----------------------
# Get order
# ----------------------
@app.get("/orders/<order_id>")
def get_order(order_id):
    order = ORDERS.get(order_id)

    if not order:
        return jsonify({"error": "Order not found"}), 200

    return jsonify({
        "orderId": order_id,
        **order
    })


# ----------------------
# App entry
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)
