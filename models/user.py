# Lib
from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    username: str = Field(examples = ["john_doe"], description="Username of the account")
    password: str = Field(examples = ["john_wick"], description="Password of the account")
    tags: Optional[list] = Field(examples = [["coding", "gaming"]], description="List of tags user is interested in")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
