from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.db.database import get_db
from app.models.news import NewsArticle
from fastapi.responses import HTMLResponse
from app.models.category import Category
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="src/app/templates")

@router.get("/", response_class=HTMLResponse)
def homepage(request: Request, db: Session = Depends(get_db)):
    latest_news = db.query(NewsArticle).order_by(NewsArticle.created_at.desc()).limit(10).all()
    categories = db.query(Category).all()
    
    return templates.TemplateResponse("home.html", {
        "request": request,
        "latest_news": latest_news,
        "categories": categories,
        "today": datetime.now()
    })
