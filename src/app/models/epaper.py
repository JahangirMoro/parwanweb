# src/app/models/epaper.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.database import Base

class EpaperFile(Base):
    __tablename__ = "epaper_files"

    id = Column(Integer, primary_key=True, index=True)
    edition_id = Column(Integer, ForeignKey("editions.id"), nullable=False)
    date = Column(Date, nullable=False)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    edition = relationship("Edition", back_populates="epapers")
