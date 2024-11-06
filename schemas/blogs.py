from pydantic import BaseModel

class BlogBase(BaseModel):
    blog_title: str
    desc: str

class BlogCreate(BlogBase):
    pass

class BlogView(BlogBase):
    id: str