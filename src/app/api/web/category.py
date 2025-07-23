from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.news import NewsArticle
from app.models.category import Category

router = APIRouter()
templates = Jinja2Templates(directory="src/app/templates")
#for categories only click on category name and page will be loaded with all articles of that category
#this is for web side rendering of category page
@router.get("/category/{category_id}")
def category_page(category_id: int, request: Request, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

    articles = db.query(NewsArticle).filter(NewsArticle.category_id == category_id)\
                                    .order_by(NewsArticle.created_at.desc()).all()
    categories = db.query(Category).all()

    return templates.TemplateResponse("category.html", {
        "request": request,
        "category": category,
        "articles": articles,
        "categories": categories
    })
# src/app/api/web/category.py