# ✅ api/web/contact.py

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.contact import ContactInfo  # ✅ correct import

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/contact")
def contact_page(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@router.post("/contact")
def submit_contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    db: Session = Depends(get_db)
):
    new_contact = ContactInfo(name=name, email=email, message=message)
    db.add(new_contact)
    db.commit()
    return templates.TemplateResponse("contact.html", {
        "request": request,
        "success": "آپ کا پیغام موصول ہو گیا ہے۔ شکریہ!"
    })
