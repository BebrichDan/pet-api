from pydantic import BaseModel, Field
from typing import Optional


class BookSchema(BaseModel):
    title: str
    author: str

class BookGetSchema(BaseModel):
    id: int
    title: str
    author: str

class BookUpdateSchema(BaseModel):
    id: Optional[int] = Field(default=None)
    title: str
    author: str

class BookPatchSchema(BaseModel):
    title: Optional[str] = Field(default=None)
    author: Optional[str] = Field(default=None)