from typing import Optional

from pydantic import BaseModel
from datetime import datetime, date
import uuid

class Book(BaseModel) :
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    published_date: date
    language: str
    created_at: datetime
    update_at: datetime

class BookCreateModel (BaseModel) :
    title: str
    author: str
    publisher: str
    published_date: str
    language: str


class BookUpdateModel(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    language: Optional[str] = None
