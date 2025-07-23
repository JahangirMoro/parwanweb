from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    news_articles = relationship("NewsArticle", back_populates="category")
