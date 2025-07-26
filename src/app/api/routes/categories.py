import os
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models import Category
from starlette.status import HTTP_302_FOUND

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# ======================
# List Categories
# ======================
@router.get("/admin/categories")
def list_categories(request: Request, db: Session = Depends(get_db)):
    categories = db.query(Category).order_by(Category.id.desc()).all()
    return templates.TemplateResponse("admin/categories/list.html", {
        "request": request,
        "categories": categories
    })


# ======================
# Create Category (GET + POST)
# ======================
@router.get("/admin/categories/create")
def create_category_form(request: Request):
    return templates.TemplateResponse("admin/categories/create.html", {
        "request": request
    })

@router.post("/admin/categories/create")
def create_category(name: str = Form(...), db: Session = Depends(get_db)):
    new_cat = Category(name=name)
    db.add(new_cat)
    db.commit()
    return RedirectResponse("/admin/categories", status_code=HTTP_302_FOUND)


# ======================
# Edit Category (GET + POST)
# ======================
@router.get("/admin/categories/edit/{category_id}")
def edit_category_form(category_id: int, request: Request, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        return RedirectResponse("/admin/categories", status_code=HTTP_302_FOUND)
    return templates.TemplateResponse("admin/categories/edit.html", {
        "request": request,
        "category": category
    })

@router.post("/admin/categories/edit/{category_id}")
def update_category(category_id: int, name: str = Form(...), db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        category.name = name
        db.commit()
    return RedirectResponse("/admin/categories", status_code=HTTP_302_FOUND)


# ======================
# Delete Category
# ======================
@router.get("/admin/categories/delete/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
    return RedirectResponse("/admin/categories", status_code=HTTP_302_FOUND)
