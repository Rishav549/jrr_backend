from pydantic import BaseModel
import datetime

class ProductBase(BaseModel):
    product_name: str
    desc: str

class ProductCreate(ProductBase):
    pass
    
class ProductView(ProductBase):
    id: str
