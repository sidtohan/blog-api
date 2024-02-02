# Lib
from pydantic import BaseModel, Field
from typing import Optional

class Blog(BaseModel):
    title: str = Field(examples=["FastAPI is good"], description="Title of the blog")
    content: str = Field(examples=["Lorem ipsum ......"], description="Content of the blog")
    tags: Optional[list] = Field(examples=[["coding", "gaming"]])

class BlogInDb(Blog):
    by: str = Field(examples=["john_doe"], description="Username of the user who wrote the blog")
    by_id: str = Field(description="ID of the user who created this blog")
    by_photo: str = Field(None, examples=["https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg"], description="URL of the profile picture of the user")
    likes: int = Field(0, description="Number of likes of blog")    