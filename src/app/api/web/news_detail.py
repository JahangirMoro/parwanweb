from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.news import NewsArticle
from fastapi.responses import HTMLResponse
#for rendring html for news details page
from app.models.category import Category  # ✅ IMPORT required
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/news/{article_id}", response_class=HTMLResponse)
def news_detail(article_id: int, request: Request, db: Session = Depends(get_db)):
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="خبر نہیں ملی")

    categories = db.query(Category).all()  # ✅ All categories for navbar etc.

    return templates.TemplateResponse("news_detail.html", {
        "request": request,
        "article": article,
        "categories": categories  # ✅ Pass categories to the template
    })