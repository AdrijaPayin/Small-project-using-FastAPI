from fastapi import FastAPI
from models import Product

app = FastAPI()

@app.get("/")
def greet():
    return {"message": "welcome"}

products = [
    Product(id=1, name="iPhone 15", description="Apple smartphone with A16 Bionic chip", price=79999.0, quantity=15),
    Product(id=2, name="Samsung Galaxy S24", description="Android flagship smartphone", price=74999.0, quantity=20),
    Product(id=3, name="Sony WH-1000XM5", description="Noise-cancelling wireless headphones", price=29999.0, quantity=12),
    Product(id=4, name="Dell XPS 13", description="13-inch premium ultrabook laptop", price=119999.0, quantity=8),
    Product(id=5, name="Apple iPad Air", description="10.9-inch tablet with M2 chip", price=59999.0, quantity=10),
    Product(id=6, name="Logitech MX Master 3S", description="Wireless productivity mouse", price=9999.0, quantity=25),
    Product(id=7, name="Samsung 27-inch Monitor", description="QHD IPS display monitor", price=22999.0, quantity=14),
    Product(id=8, name="JBL Flip 6", description="Portable Bluetooth speaker", price=8999.0, quantity=18),
    Product(id=9, name="Canon EOS R50", description="Mirrorless camera for photography", price=68999.0, quantity=7),
    Product(id=10, name="ASUS ROG Strix G16", description="Gaming laptop with RTX graphics", price=139999.0, quantity=5)
]

@app.get("/products", response_model=list[Product])
def show_products():
    return products

@app.get("/products/{id}")
def get_product(id: int):
    for product in products:
        if product.id == id:
            return product
    return {"error": "Product not found"}