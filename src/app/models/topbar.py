from sqlalchemy import Column, Integer, String
from app.db.base import Base

class TopBar(Base):
    __tablename__ = "top_bar"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(255), nullable=False)
