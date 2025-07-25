from fastapi import APIRouter, Depends, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from math import ceil

from app.db.session import get_db
from app.models.news import NewsArticle
from app.models.category import Category
from app.models.edition import Edition

router = APIRouter()
templates = Jinja2Templates(directory="src/app/templates")

@router.get("/", response_class=HTMLResponse)
def homepage(
    request: Request,
    
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1)
):
    # ✅ All categories
    categories = db.query(Category).all()

    # ✅ All editions (e.g. Karachi, Nawabshah)
    editions = db.query(Edition).order_by(Edition.created_at.desc()).all()

    # ✅ Pagination: 6 news per page
    page_size = 6
    total_articles = db.query(NewsArticle).count()
    total_pages = ceil(total_articles / page_size)
    offset = (page - 1) * page_size

    latest_news = (
        db.query(NewsArticle)
        .order_by(NewsArticle.created_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    # ✅ Category-wise 4 latest news
    category_articles = {
        category: db.query(NewsArticle)
            .filter(NewsArticle.category_id == category.id)
            .order_by(NewsArticle.created_at.desc())
            .limit(4)
            .all()
        for category in categories
    }

    return templates.TemplateResponse("home.html", {
        "request": request,
        "categories": categories,
        "editions": editions,
        "latest_news": latest_news,
        "category_articles": category_articles,
        "page": page,
        "total_pages": total_pages
    })
