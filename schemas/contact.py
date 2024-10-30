from pydantic import BaseModel
from bson import ObjectId

class ContactBase(BaseModel):
    full_name: str
    email_id: str
    contact_number: str
    hsn_code: str
    message: str

class ContactCreate(ContactBase):
    pass

class ContactView(ContactBase):
    id: str