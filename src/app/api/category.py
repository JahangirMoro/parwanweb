from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.category import *
from app.db import get_db
from app.services import category as category_service

router = APIRouter()

@router.post("/", response_model=CategoryOut)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return category_service.create_category(db, category)

@router.get("/", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return category_service.get_categories(db)

@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    db_category = category_service.get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    return category_service.update_category(db, category_id, category)

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category_service.delete_category(db, category_id)
    return {"message": "Category deleted"}
