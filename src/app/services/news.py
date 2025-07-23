from sqlalchemy.orm import Session
from app.models import NewsArticle
from app.schemas.news import NewsCreate, NewsUpdate

def create_news_article(db: Session, article: NewsCreate):
    db_article = NewsArticle(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def get_all_articles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(NewsArticle).offset(skip).limit(limit).all()

def get_article_by_id(db: Session, article_id: int):  # 👈 Missing function
    return db.query(NewsArticle).filter(NewsArticle.id == article_id).first()

def update_article(db: Session, article_id: int, article_update: NewsUpdate):
    db_article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if not db_article:
        return None
    for key, value in article_update.dict(exclude_unset=True).items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article

def delete_article(db: Session, article_id: int):
    db_article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if not db_article:
        return False
    db.delete(db_article)
    db.commit()
    return True
