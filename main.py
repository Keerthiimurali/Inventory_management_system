from fastapi import Depends,FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session, engine
import database_models 
from sqlalchemy.orm import Session

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://localhost:3001",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)

@app.get("/")
def greet():
    return "welcome to  Inventory Management System"

products = [
    Product(id=1,name="phone",description= "A Smartphone",price=699.99, quantity=50),
    Product(id=2,name="laptop", description= "A Powerful laptop", price= 999.99, quantity=30),
    Product(id=3,name="pen", description= "A blue ink pen", price= 1.99, quantity=100),
    Product(id=4,name="Table", description= "A Wooden table", price= 199.99, quantity=20)
    
    
]

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db=session()
    try:
        count = db.query(database_models.Product).count()
        if count == 0:
            for product in products:
                db.add(database_models.Product(**product.model_dump()))
            db.commit()
    finally:
        db.close()
        
init_db()


@app.get("/products")
def get_all_products(db:Session =Depends(get_db)):
   #since the above line of code db:Session =Depends(get_db)), we dont want the below line that is db=session()
    #db connection
    #query
   # db = session()
    #db.query
    db_products = db.query(database_models.Product).all()
    return db_products

@app.get("/products/{id}")
def get_product_by_id(id:int, db:Session =Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        return db_product
    return "product not found"

@app.post("/products")
def add_product(product:Product, db:Session =Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{id}")
def update_product(id:int, product:Product, db:Session =Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price =product.price
        db_product.quantity = product.quantity
        db.commit()
        return "Product updated"
    else:
        return "no product found"
        


@app.delete("/products/{id}")
def delete_product(id:int, db:Session =Depends(get_db)):
    #fetch the product from the database, wherever u have the id in the parameter, below code
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted"
    else:
        return "no product found"
