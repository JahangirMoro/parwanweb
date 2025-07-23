from fastapi import APIRouter, Request, Depends, Query
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date
from app.db.session import get_db
from app.models.news import NewsArticle
from app.models.category import Category
from app.models.edition import Edition

router = APIRouter()
templates = Jinja2Templates(directory="src/app/templates")

@router.get("/archive")
def archive_view(
    request: Request,
    selected_date: date = Query(None),
    db: Session = Depends(get_db)
):
    categories = db.query(Category).all()
    editions = db.query(Edition).order_by(Edition.created_at.desc()).all()

    news_query = db.query(NewsArticle)

    if selected_date:
        news_query = news_query.filter(
            NewsArticle.created_at >= selected_date,
            NewsArticle.created_at < selected_date.replace(day=selected_date.day + 1)
        )

    news_list = news_query.order_by(NewsArticle.created_at.desc()).all()

    return templates.TemplateResponse("archive.html", {
        "request": request,
        "categories": categories,
        "editions": editions,
        "selected_date": selected_date,
        "news_list": news_list
    })
