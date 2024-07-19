from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample data
users = {
    1: {"name": "John Doe"},
    2: {"name": "Jane Smith"}
}

products = {
    1: {"name": "Product 1", "price": 10, "inventory": 100},
    2: {"name": "Product 2", "price": 20, "inventory": 50}
}

orders = []

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    user_id = data.get('user_id')
    cart_items = data.get('cart_items')  

    if user_id not in users:
        return jsonify({"error": "Invalid user ID"}), 400

    total_amount = 0
    for product_id, quantity in cart_items.items():
        if product_id not in products:
            return jsonify({"error": f"Product {product_id} not found"}), 400
        
        product = products[product_id]
        if product["inventory"] < quantity:
            return jsonify({"error": f"Insufficient inventory for product {product_id}"}), 400

        total_amount += product["price"] * quantity
        products[product_id]["inventory"] -= quantity  

    order = {
        "user_id": user_id,
        "items": cart_items,
        "total_amount": total_amount
    }
    orders.append(order)

    return jsonify({"message": "Checkout successful", "order": order}), 200

if __name__ == '__main__':
    app.run(debug=True)
