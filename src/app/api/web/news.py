# src/app/api/web/news.py
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.news import NewsArticle
from app.models.category import Category

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/news/{news_id}")
def news_detail(news_id: int, request: Request, db: Session = Depends(get_db)):
    article = db.query(NewsArticle).filter(NewsArticle.id == news_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="خبر نہیں ملی")
    
    categories = db.query(Category).all()

    return templates.TemplateResponse("news_detail.html", {
        "request": request,
        "article": article,
        "categories": categories
    })
