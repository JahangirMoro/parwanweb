import os
from uuid import uuid4
from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import date
from app.db.database import get_db
from app.models.edition import Edition
from app.models.epaper import EpaperFile

router = APIRouter()
templates = Jinja2Templates(directory="src/app/templates")
EPAPER_DIR = "uploads/epapers"
os.makedirs(EPAPER_DIR, exist_ok=True)

@router.get("/admin/epaper/upload")
def upload_form(request: Request, db: Session = Depends(get_db)):
    editions = db.query(Edition).all()
    return templates.TemplateResponse("admin/epaper/upload.html", {"request": request, "editions": editions})

@router.post("/admin/epaper/upload")
async def upload_epaper(
    date: date = Form(...),
    edition_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    filename = f"{uuid4().hex}_{file.filename}"
    filepath = os.path.join(EPAPER_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(await file.read())

    epaper = EpaperFile(date=date, edition_id=edition_id, file_path=filepath)
    db.add(epaper)
    db.commit()
    return RedirectResponse("/admin/epaper/upload", status_code=303)
