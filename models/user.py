# Lib
from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    username: str = Field(examples = ["john_doe"], description="Username of the account")
    password: str = Field(examples = ["john_wick"], description="Password of the account")
    tags: Optional[list] = Field([], examples = [["coding", "gaming"]], description="List of tags user is interested in")
    photo: Optional[str] = Field(None, examples=["https://images.pexels.com/photos/45201/kitty-cat-kitten-pet-45201.jpeg"])
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
