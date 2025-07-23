from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import NewsArticle
import os

router = APIRouter()
templates = Jinja2Templates(directory="src/app/templates")  # Make sure this path matches your project

@router.get("/news/{article_id}")
def article_detail(article_id: int, request: Request, db: Session = Depends(get_db)):
    # Article fetch karo
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    
    # Agar article na mile toh 404 return karo
    if not article:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

    # Warna detail template render karo
    return templates.TemplateResponse("news/article_detail.html", {
        "request": request,
        "article": article
    })


# src/app/api/routes/frontend.py
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.news import NewsArticle
from app.models.category import Category

router = APIRouter()
templates = Jinja2Templates(directory="src/app/templates")

@router.get("/")
def homepage(request: Request, db: Session = Depends(get_db)):
    articles = db.query(NewsArticle).order_by(NewsArticle.created_at.desc()).limit(10).all()
    categories = db.query(Category).all()
    return templates.TemplateResponse("home.html", {
        "request": request,
        "articles": articles,
        "categories": categories
    })
