# news_service.py for services module
from sqlalchemy.orm import Session
from app.models.news import NewsArticle
from app.schemas.news import NewsArticleCreate

def create_article(db: Session, article_data: NewsArticleCreate) -> NewsArticle:
    article = NewsArticle(**article_data.dict())
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

def get_all_articles(db: Session):
    return db.query(NewsArticle).order_by(NewsArticle.created_at.desc()).all()
