import os
from uuid import uuid4
from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import NewsArticle, Category, Edition

# Setup
router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ======================
# Admin Dashboard
# ======================

@router.get("/admin/")
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    try:
        total_articles = db.query(NewsArticle).count()
        total_categories = db.query(Category).count()
        total_editions = db.query(Edition).count()

        recent_articles = (
            db.query(NewsArticle)
            .order_by(NewsArticle.created_at.desc())
            .limit(5)
            .all()
        )

        return templates.TemplateResponse("admin/dashboard.html", {
            "request": request,
            "total_articles": total_articles,
            "total_categories": total_categories,
            "total_editions": total_editions,
            "recent_articles": recent_articles
        })

    except Exception as e:
        return templates.TemplateResponse("500.html", {
            "request": request,
            "error": str(e)
        }, status_code=500)

# ======================
# Article List
# ======================

@router.get("/admin/articles")
def admin_articles(request: Request, db: Session = Depends(get_db)):
    articles = db.query(NewsArticle).order_by(NewsArticle.created_at.desc()).all()
    return templates.TemplateResponse("admin/articles/list.html", {
        "request": request,
        "articles": articles
    })


# ======================
# Create Article (GET + POST)
# ======================

@router.get("/admin/articles/create")
def admin_create_article_form(request: Request, db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return templates.TemplateResponse("admin/articles/create.html", {
        "request": request,
        "categories": categories
    })

@router.post("/admin/articles/create")
async def admin_create_article(
    title: str = Form(...),
    summary: str = Form(...),
    content: str = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    filename = f"{uuid4().hex}_{image.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as f:
        f.write(await image.read())

    article = NewsArticle(
        title=title,
        summary=summary,
        content=content,
        category_id=category_id,
        image_url=file_path,
    )
    db.add(article)
    db.commit()
    db.refresh(article)

    return RedirectResponse("/admin/articles", status_code=303)


# ======================
# Edit Article (GET + POST)
# ======================

@router.get("/admin/articles/edit/{article_id}")
def edit_article_form(article_id: int, request: Request, db: Session = Depends(get_db)):
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    categories = db.query(Category).all()
    
    if not article:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    
    return templates.TemplateResponse("admin/articles/edit.html", {
        "request": request,
        "article": article,
        "categories": categories
    })

@router.post("/admin/articles/edit/{article_id}")
async def update_article(
    article_id: int,
    title: str = Form(...),
    summary: str = Form(...),
    content: str = Form(...),
    category_id: int = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if not article:
        return {"error": "Article not found"}

    article.title = title
    article.summary = summary
    article.content = content
    article.category_id = category_id

    if image:
        filename = f"{uuid4().hex}_{image.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(await image.read())
        article.image_url = file_path

    db.commit()
    db.refresh(article)

    return RedirectResponse("/admin/articles", status_code=303)


# ======================
# Delete Article
# ======================

@router.get("/admin/articles/delete/{article_id}")
def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(NewsArticle).filter(NewsArticle.id == article_id).first()
    if article:
        db.delete(article)
        db.commit()
    return RedirectResponse("/admin/articles", status_code=303)
