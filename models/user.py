# Lib
from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    username: str = Field(examples = ["john_doe"])
    password: str = Field(examples = ["john_wick"])
    photo: Optional[str] = Field(default = None, examples = ["https://google.com"])

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserLR(BaseModel):
    username: str = Field(examples = ["john_doe"])
    password: str = Field(examples = ["john_wick"])