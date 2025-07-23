from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.edition import Edition
from datetime import date

router = APIRouter()
templates = Jinja2Templates(directory="src/app/templates")

# ✅ User-facing route: PDF redirect
@router.get("/epaper/{edition_id}/today", tags=["Epaper Redirect"])
def redirect_today_edition_pdf(edition_id: int, db: Session = Depends(get_db)):
    today = date.today()
    edition = (
        db.query(Edition)
        .filter(Edition.id == edition_id, Edition.date == today)
        .first()
    )
    if not edition:
        return RedirectResponse(url="/not-found", status_code=302)

    return RedirectResponse(url=f"/{edition.pdf_url}", status_code=302)

# ✅ Admin view route
@router.get("/admin/epaper/{edition_id}/today")
def show_today_edition_admin(edition_id: int, request: Request, db: Session = Depends(get_db)):
    today = date.today()
    edition = (
        db.query(Edition)
        .filter(Edition.id == edition_id, Edition.date == today)
        .first()
    )
    if not edition:
        return templates.TemplateResponse("admin/not_found.html", {"request": request}, status_code=404)

    return templates.TemplateResponse("admin/epaper/view.html", {
        "request": request,
        "edition": edition
    })
