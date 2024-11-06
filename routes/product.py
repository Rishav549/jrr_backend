from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from db.db import get_db, DB
from schemas.product import ProductBase, ProductCreate, ProductView
from bson import ObjectId
from datetime import datetime
from models.product import Product
import os
import uuid

router = APIRouter()
UPLOAD_DIRECTORY = "./uploaded_images/products"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/product/create")
async def create_product(product_name: str = Form(...),
    desc: str = Form(...),
    images: list[UploadFile] = File(...), 
    db: DB= Depends(get_db)):
    existing_product = db.find_one("product_master", {"product_code": product_name})
    if existing_product is not None:
        return JSONResponse({"detail": "product already exists"}, status_code=400)

    image_paths = []
    for image in images:
        unique_filename = f"{uuid.uuid4()}.png"
        image_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)
        with open(image_path, "wb") as buffer:
            buffer.write(await image.read())
        image_paths.append(image_path)

    # Create product data to insert
    product_data = {
        "product_name": product_name,
        "desc": desc,
        "image": image_paths
    }

    # Insert into MongoDB
    inserted_product = db.insert("product_master", product_data)

    #product = db.insert("product_master", product.model_dump(mode="json"))
    return JSONResponse({"detail": "ok", "product": inserted_product}, status_code=201)


@router.get("/product/")
async def get_product(db: DB = Depends(get_db)):
    products_cursor = db.find("product_master", {})
    products = [Product.from_document(product) for product in products_cursor]
    if not products:
        return JSONResponse({"detail": "Products not found"}, status_code=404)
    
    return {"detail": "ok", "products": [product.to_dict() for product in products]}


@router.get("/product/{product_id}")
async def get_product_by_id(product_id: str, db: DB = Depends(get_db)):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID format")
    
    product_document = db.find_one("product_master", {"_id": ObjectId(product_id)})
    if not product_document:
        return JSONResponse({"detail": "Product Not Found"}, status_code=404)

    product = Product.from_document(product_document)
    return {"detail": "ok", "product": product.to_dict()}