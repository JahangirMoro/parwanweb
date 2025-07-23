#from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey , relationship
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship  # ✅ this is correct

from sqlalchemy.sql import func
from app.db.base import Base

class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)  # 👈 یہ لائن add کریں
    category = relationship("Category", back_populates="news_articles")
    image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
