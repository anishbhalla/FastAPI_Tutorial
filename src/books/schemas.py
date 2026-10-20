# Book schema using Pydantic
from typing import Optional

from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str

# Book update schema using Pydantic
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[str] = None
