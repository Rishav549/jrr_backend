from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from db.db import get_db, DB
from models.blogs import Blogs
from bson import ObjectId
import os
import uuid
from utilities.auth import get_current_user

router = APIRouter()

UPLOAD_DIRECTORY="./uploaded_images/blogs"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.post("/blogs/create")
async def create_blogs(blog_title: str = Form(...),
    desc: str = Form(...),
    image: UploadFile = File(...), 
    db: DB= Depends(get_db), user: dict = Depends(get_current_user)):

    unique_filename = f"{uuid.uuid4()}.png"
    image_path = os.path.join(UPLOAD_DIRECTORY, unique_filename)
    with open(image_path, "wb") as buffer:
        buffer.write(await image.read())
        
    blog_data ={
        "blog_title": blog_title,
        "desc": desc,
        "image": image_path
    }

    inserted_blog = db.insert("blog_master", blog_data)

    return JSONResponse({"detail": "ok", "product": inserted_blog}, status_code=201)

@router.get("/blogs/")
async def get_blogs(db: DB=Depends(get_db)):
    blogs_cursor = db.find("blog_master",{})
    blogs = [Blogs.from_document(blog) for blog in blogs_cursor]
    if not blogs:
        return JSONResponse({"detail": "Blogs not found"}, status_code=404)
    
    return {"detail": "ok", "blogs": [blog.to_dict() for blog in blogs]}


@router.get("/blog/{blog_id}")
async def get_blog_by_id(blog_id:str, db: DB=Depends(get_db)):
    if not ObjectId.is_valid(blog_id):
        raise HTTPException(status_code=400, detail="Invalid blog ID format")
    
    blog_document = db.find_one("blog_master", {"_id": ObjectId(blog_id)})
    if not blog_document:
        return JSONResponse({"detail": "Blog Not Found"}, status_code=404)

    blog = Blogs.from_document(blog_document)
    return {"detail": "ok", "blog": blog.to_dict()}