from sqlalchemy import Column, Integer, String, Date, DateTime
from datetime import datetime
from app.db.database import Base

class Edition(Base):
    __tablename__ = "editions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    image_url = Column(String, nullable=False)
    pdf_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
