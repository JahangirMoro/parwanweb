from fastapi import APIRouter, Depends, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from math import ceil
from pathlib import Path
import os

from app.db.session import get_db
from app.models.news import NewsArticle
from app.models.category import Category
from app.models.edition import Edition

router = APIRouter()

# ✅ Base path
BASE_DIR = Path(__file__).resolve()

# ✅ Check if running on Render (PROD) or local
# Render usually sets `RENDER` or `RENDER_EXTERNAL_HOSTNAME`
IS_RENDER = os.getenv("RENDER") or os.getenv("RENDER_EXTERNAL_HOSTNAME")

# ✅ Template path (Render: src removed, Local: includes src)
if IS_RENDER:
    templates_path = Path("app/templates")   # for Render
else:
    templates_path = Path("src/app/templates")  # for local

templates = Jinja2Templates(directory=str(templates_path))


@router.get("/", response_class=HTMLResponse)
def homepage(
    request: Request,
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1)
):
    categories = db.query(Category).all()
    editions = db.query(Edition).order_by(Edition.created_at.desc()).all()

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
