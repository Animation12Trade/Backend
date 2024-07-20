from app import app
from models import db, User, Product

def seed_data():
    with app.app_context():
        user1 = User(name="John Doe")
        user2 = User(name="Jane Smith")

        product1 = Product(name="Product 1", price=10.0, inventory=100)
        product2 = Product(name="Product 2", price=20.0, inventory=50)

        db.session.add_all([user1, user2, product1, product2])
        db.session.commit()

if __name__ == '__main__':
    seed_data()
