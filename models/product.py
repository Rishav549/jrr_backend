from bson import ObjectId
from datetime import datetime

class Product:
    def __init__(self, _id: ObjectId, product_name: str, desc: str, image: list[str]):
        self._id = _id
        self.product_name = product_name
        self.desc = desc
        self.image = image

    def to_dict(self):
        return {
            "_id": str(self._id),
            "product_name": self.product_name,
            "desc": self.desc,
            "image": self.image
        }

    @staticmethod
    def from_document(document):
        return Product(
            _id=document["_id"],
            product_name=document["product_name"],
            desc=document["desc"],
            image=document["image"]
        )
