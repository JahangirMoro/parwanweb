from pydantic import BaseModel
from datetime import datetime

class EditionBase(BaseModel):
    name: str

class EditionCreate(EditionBase):
    pass

class EditionOut(EditionBase):
    id: int
    image_url: str | None
    pdf_url: str | None
    created_at: datetime

    class Config:
         model_config = {
        "from_attributes": True
    }