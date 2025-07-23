# src/app/api/routes/public.py

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.news import NewsArticle

router = APIRouter()
templates = Jinja2Templates(directory="src/app/templates")

@router.get("/")
def homepage(request: Request, db: Session = Depends(get_db)):
    latest_articles = db.query(NewsArticle).order_by(NewsArticle.created_at.desc()).limit(10).all()
    main_headline = latest_articles[0] if latest_articles else None
    side_articles = latest_articles[1:6] if len(latest_articles) > 1 else []

    return templates.TemplateResponse("home.html", {
        "request": request,
        "main_headline": main_headline,
        "side_articles": side_articles,
        "latest_articles": latest_articles
    })
