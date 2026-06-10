from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models import Product  # Pydantic model
from database import session, engine
import database_models     # SQLAlchemy model

# Create database tables if they don't exist
database_models.Base.metadata.create_all(bind=engine)

# Sample seeding data
SAMPLE_PRODUCTS = [
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

def init_db():
    """Seeds the PostgreSQL database if it is empty."""
    db = session()
    try:
        existing_count = db.query(database_models.Product).count()
        if existing_count == 0:
            for product in SAMPLE_PRODUCTS:
                db.add(database_models.Product(**product.model_dump()))
            db.commit()
            print("💾 Database initialized with sample products.")
    finally:
        db.close()

# FastAPI Lifespan management for clean initialization
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()  # Run database seeding safely on startup
    yield

app = FastAPI(
    title="NexusCart API",
    description="A robust backend production API for inventory management.",
    version="1.0.0",
    lifespan=lifespan
)

# Database Dependency Injection
def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@app.get("/", status_code=status.HTTP_200_OK)
def greet():
    return {"status": "online", "message": "Welcome to NexusCart API"}


@app.get("/products/", status_code=status.HTTP_200_OK)
def get_all_products(db: Session = Depends(get_db)):
    return db.query(database_models.Product).all()


@app.get("/products/{product_id}", status_code=status.HTTP_200_OK)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if not product:
        # Fixed: Now properly returns a 404 HTTP Exception instead of a generic dictionary
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@app.post("/products/", status_code=status.HTTP_201_CREATED)
def create_product(product: Product, db: Session = Depends(get_db)):
    new_product = database_models.Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product created successfully", "product": new_product}


@app.put("/products/{product_id}", status_code=status.HTTP_200_OK)
def update_product(product_id: int, product: Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.quantity = product.quantity
    
    db.commit()
    db.refresh(db_product)
    return {"message": "Product updated successfully", "product": db_product}


@app.delete("/products/{product_id}", status_code=status.HTTP_200_OK)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"message": f"Product #{product_id} deleted successfully"}
