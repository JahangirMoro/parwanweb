from sqlalchemy import Column, Integer, String, Text, DateTime, func
from app.db import Base

class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    role = Column(String(50), default='admin')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
