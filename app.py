from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, User, Product, Order, init_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
CORS(app)

init_db(app)

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    user_id = data.get('user_id')
    cart_items = data.get('cart_items')

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Invalid user ID"}), 400

    total_amount = 0
    for product_id, quantity in cart_items.items():
        product = Product.query.get(product_id)
        if not product:
            return jsonify({"error": f"Product {product_id} not found"}), 400

        if product.inventory < quantity:
            return jsonify({"error": f"Insufficient inventory for product {product_id}"}), 400

        total_amount += product.price * quantity
        product.inventory -= quantity

    order = Order(user_id=user_id, total_amount=total_amount, items=cart_items)
    db.session.add(order)
    db.session.commit()

    return jsonify({"message": "Checkout successful", "order": order.to_dict()}), 200

if __name__ == '__main__':
    app.run(debug=True)
