from bson import ObjectId
from datetime import datetime

class Contact:
    def __init__(self, _id: ObjectId, full_name: str, email_id: str, contact_number: str, hsn_code: str|None, message: str):
        self._id = _id
        self.full_name = full_name
        self.email_id = email_id
        self.contact_number = contact_number
        self.hsn_code = hsn_code
        self.message = message

    def to_dict(self):
        return {
            "_id": str(self._id),
            "full_name": self.full_name,
            "email_id": self.email_id,
            "contact_number": self.contact_number,
            "hsn_code": self.hsn_code,
            "message": self.message
        }

    @staticmethod
    def from_document(document):
        return Contact(
            _id=document["_id"],
            full_name=document["full_name"],
            email_id=document["email_id"],
            contact_number=document["contact_number"],
            hsn_code=document["hsn_code"] if "hsn_code" in document else None,
            message=document["message"]
        )