import os
from uuid import uuid4
from datetime import date
from fastapi import APIRouter, Request, Depends, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.edition import Edition

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

UPLOAD_IMAGE_DIR = "uploads/editions/images"
UPLOAD_PDF_DIR = "uploads/editions/pdfs"
os.makedirs(UPLOAD_IMAGE_DIR, exist_ok=True)
os.makedirs(UPLOAD_PDF_DIR, exist_ok=True)

# =====================
# List Editions
# =====================
@router.get("/admin/editions")
def list_editions(request: Request, db: Session = Depends(get_db)):
    editions = db.query(Edition).order_by(Edition.date.desc()).all()
    return templates.TemplateResponse("admin/editions/list.html", {
        "request": request,
        "editions": editions
    })

# =====================
# Create Edition (GET)
# =====================
@router.get("/admin/editions/create")
def create_edition_form(request: Request):
    return templates.TemplateResponse("admin/editions/create.html", {"request": request})

# =====================
# Create Edition (POST)
# =====================
@router.post("/admin/editions/create")
async def create_edition(
    name: str = Form(...),
    date_: date = Form(...),
    image: UploadFile = File(...),
    pdf: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    image_filename = f"{uuid4().hex}_{image.filename}"
    image_path = os.path.join(UPLOAD_IMAGE_DIR, image_filename)
    with open(image_path, "wb") as f:
        f.write(await image.read())

    pdf_filename = f"{uuid4().hex}_{pdf.filename}"
    pdf_path = os.path.join(UPLOAD_PDF_DIR, pdf_filename)
    with open(pdf_path, "wb") as f:
        f.write(await pdf.read())

    edition = Edition(
        name=name,
        date=date_,
        image_url=image_path,
        pdf_url=pdf_path
    )
    db.add(edition)
    db.commit()
    return RedirectResponse("/admin/editions", status_code=303)

# =====================
# Edit Edition (GET)
# =====================
@router.get("/admin/editions/edit/{edition_id}")
def edit_edition_form(edition_id: int, request: Request, db: Session = Depends(get_db)):
    edition = db.query(Edition).filter(Edition.id == edition_id).first()
    if not edition:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("admin/editions/edit.html", {
        "request": request,
        "edition": edition
    })

# =====================
# Edit Edition (POST)
# =====================
@router.post("/admin/editions/edit/{edition_id}")
async def update_edition(
    edition_id: int,
    name: str = Form(...),
    date_: date = Form(...),
    image: UploadFile = File(None),
    pdf: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    edition = db.query(Edition).filter(Edition.id == edition_id).first()
    if not edition:
        return {"error": "Edition not found"}

    edition.name = name
    edition.date = date_

    if image:
        image_filename = f"{uuid4().hex}_{image.filename}"
        image_path = os.path.join(UPLOAD_IMAGE_DIR, image_filename)
        with open(image_path, "wb") as f:
            f.write(await image.read())
        edition.image_url = image_path

    if pdf:
        pdf_filename = f"{uuid4().hex}_{pdf.filename}"
        pdf_path = os.path.join(UPLOAD_PDF_DIR, pdf_filename)
        with open(pdf_path, "wb") as f:
            f.write(await pdf.read())
        edition.pdf_url = pdf_path

    db.commit()
    return RedirectResponse("/admin/editions", status_code=303)

# =====================
# Delete Edition
# =====================
@router.get("/admin/editions/delete/{edition_id}")
def delete_edition(edition_id: int, db: Session = Depends(get_db)):
    edition = db.query(Edition).filter(Edition.id == edition_id).first()
    if edition:
        db.delete(edition)
        db.commit()
    return RedirectResponse("/admin/editions", status_code=303)
