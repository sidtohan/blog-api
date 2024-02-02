# Lib
from pydantic import BaseModel, Field
from typing import Optional

class ReturnMessage(BaseModel):
    Message: str = Field(examples=["Operation performed successfully"],description = "Message describing the status of the requested operation")