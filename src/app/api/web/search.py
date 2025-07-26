from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from app.db.session import get_db
from app.models.news import NewsArticle
from app.models.category import Category
from sqlalchemy import or_
from math import ceil

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/search")
def search_articles(request: Request, q: str = "", page: int = 1, db: Session = Depends(get_db)):
    per_page = 6

    query = db.query(NewsArticle).filter(
        or_(
            NewsArticle.title.ilike(f"%{q}%"),
            NewsArticle.summary.ilike(f"%{q}%"),
            NewsArticle.content.ilike(f"%{q}%")
        )
    )

    total_results = query.count()
    total_pages = ceil(total_results / per_page)

    results = query.order_by(NewsArticle.created_at.desc())\
                   .offset((page - 1) * per_page)\
                   .limit(per_page)\
                   .all()

    # ✅ Get all categories for nav bar
    categories = db.query(Category).all()

    return templates.TemplateResponse("search_results.html", {
        "request": request,
        "results": results,
        "query": q,
        "page": page,
        "total_pages": total_pages,
        "total_results": total_results,
        "categories": categories  # ✅ Add this line
    })
# src/app/api/web/search.py