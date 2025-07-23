# ✅ models/contact.py
from sqlalchemy import Column, Integer, String, Text
from app.db.database import Base

class ContactInfo(Base):
    __tablename__ = "contact_info"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), nullable=False)
    message = Column(Text, nullable=False)
