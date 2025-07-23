# src/app/schemas/news.py

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NewsBase(BaseModel):
    title: str
    summary: str
    content: str
    image_url: Optional[str] = None
    category_id: int  # ✅ New field added

class NewsCreate(NewsBase):
    pass

class NewsUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None  # ✅ for update

class NewsOut(NewsBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
