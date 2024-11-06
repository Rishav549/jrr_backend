from bson import ObjectId

class Blogs:
    def __init__(self,_id:ObjectId, blog_title: str, desc: str, image: str):
        self._id=_id
        self.blog_title=blog_title
        self.desc=desc
        self.image=image

    def to_dict(self):
        return{
            "_id": str(self._id),
            "blog_name": self.blog_title,
            "desc": self.desc,
            "image": self.image
        }
    
    @staticmethod
    def from_document(document):
        return Blogs(
            _id=document["_id"],
            blog_title=document["blog_title"],
            desc=document["desc"],
            image=document["image"]
        )