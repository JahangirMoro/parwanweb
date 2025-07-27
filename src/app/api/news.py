from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.schemas.news import NewsCreate, NewsUpdate, NewsOut
from app.services import news as news_service
from app.db.session import get_db
import shutil
import uuid
import os
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import NewsArticle

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


# ✅ Create article with image upload
@router.post("/", response_model=NewsOut)
def create_article(
    title: str = Form(...),
    summary: str = Form(...),
    content: str = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Generate unique filename and save image
    image_filename = f"{uuid.uuid4().hex}_{image.filename}"
    # old path
    #image_path = os.path.join("src", "app", "static", "images", image_filename)
    image_path = os.path.join("app", "static", "images", image_filename)
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    image_url = f"/static/images/{image_filename}"

    # Create NewsCreate object for service
    article_data = NewsCreate(
        title=title,
        summary=summary,
        content=content,
        category_id=category_id,
        image_url=image_url
    )

    return news_service.create_news_article(db, article_data)


# ✅ List all articles
@router.get("/", response_model=list[NewsOut])
def list_articles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return news_service.get_all_articles(db, skip, limit)


# ✅ Get article by ID this is where we c
#@router.get("/{article_id}", response_model=NewsOut)
#def get_article(article_id: int, db: Session = Depends(get_db)):
  #  article = news_service.get_article_by_id(db, article_id)
   # if not article:
    #    raise HTTPException(status_code=404, detail="Article naaaot found")
    #return article


# ✅ Update article
@router.put("/{article_id}", response_model=NewsOut)
def update_article(article_id: int, article: NewsUpdate, db: Session = Depends(get_db)):
    updated = news_service.update_article(db, article_id, article)
    if not updated:
        raise HTTPException(status_code=404, detail="Article not found")
    return updated


# ✅ Delete article
@router.delete("/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    deleted = news_service.delete_article(db, article_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"detail": "Article deleted"}




@router.get("/")
def homepage(request: Request, db: Session = Depends(get_db)):
    articles = db.query(NewsArticle).order_by(NewsArticle.created_at.desc()).limit(9).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "articles": articles
    })

@router.get("/news/{article_id}")
def article_detail(article_id: int, request: Request, db: Session = Depends(get_db)):
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if not article:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("news/article_detail.html", {
        "request": request,
        "article": article
    })
