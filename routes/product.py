from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from db.db import get_db, DB
from schemas.product import ProductBase, ProductCreate, ProductView
from bson import ObjectId
from datetime import datetime
from models.product import Product

router = APIRouter()

@router.post("/product/create")
async def create_product(product: ProductCreate, db: DB= Depends(get_db)):
    existing_product = db.find_one("product_master", {"product_code": product.product_name})
    if existing_product is not None:
        return JSONResponse({"detail": "product already exists"}, status_code=400)

    product = db.insert("product_master", product.model_dump(mode="json"))
    return JSONResponse({"detail": "ok", "product": product}, status_code=201)


@router.get("/product/")
async def get_product(db: DB = Depends(get_db)):
    products_cursor = db.find("product_master", {})
    products = [Product.from_document(product) for product in products_cursor]
    if not products:
        return JSONResponse({"detail": "Products not found"}, status_code=404)
    
    return {"detail": "ok", "products": [product.to_dict() for product in products]}