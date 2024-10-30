from fastapi import APIRouter,Depends,HTTPException
from fastapi.responses import JSONResponse
from db.db import get_db,DB
from schemas.contact import ContactBase,ContactCreate, ContactView
from bson import ObjectId
from models.contact import Contact

router = APIRouter()

@router.post("/contact/create")
async def create_contact(contact: ContactCreate, db: DB= Depends(get_db)):
    contact = db.insert("contact_master", contact.model_dump(mode="json"))
    return JSONResponse({"detail": "ok", "contact": contact}, status_code=201)

@router.get("/contact/")
async def get_contact(db: DB = Depends(get_db)):
    contact_cursor = db.find("contact_master", {})
    contacts = [Contact.from_document(contact) for contact in contact_cursor]
    if not contacts:
        return JSONResponse({"detail": "Contacts not found"}, status_code=404)
    
    return {"detail": "ok", "contacts": [contact.to_dict() for contact in contacts]}