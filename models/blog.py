# Lib
from pydantic import BaseModel, Field
from typing import Optional, List
import datetime

class Blog(BaseModel):
    title: str = Field(examples=["FastAPI is good"], description="Title of the blog")
    content: str = Field(examples=["Lorem ipsum ......"], description="Content of the blog")
    tags: Optional[list] = Field(examples=[["coding", "gaming"]])

class BlogInDb(Blog):
    by: str = Field(examples=["john_doe"], description="Username of the user who wrote the blog")
    by_id: str = Field(description="ID of the user who created this blog")
    by_photo: str = Field(None, examples=["https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg"], description="URL of the profile picture of the user")
    liked: List[str] = Field([], description="List of user IDs that have liked a particular blog")
    id: str = Field(description="ID of the blog")
    date: datetime.datetime = Field(examples=["2024-02-12T13:33:51.200+00:00"],description="Date and time of creation of the blog")
    