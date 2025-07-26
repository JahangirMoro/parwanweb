from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse

from app.db.session import get_db
from app.models.admin_user import AdminUser

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/admin/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("admin/admin_login.html", {"request": request})

@router.post("/admin/login")
def login_submit(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(AdminUser).filter(AdminUser.username == username).first()

    # 🔓 Plain text password comparison
    if user and password == user.password_hash:
        response = RedirectResponse(url="/admin/dashboard", status_code=302)
        response.set_cookie(key="admin_user", value=str(user.id), httponly=True)
        return response

    return templates.TemplateResponse("admin/admin_login.html", {
        "request": request,
        "error": "غلط یوزرنیم یا پاسورڈ"
    })
@router.get("/admin/logout")
def admin_logout():
    response = RedirectResponse(url="/admin/login", status_code=302)
    response.delete_cookie("admin_user")
    return response
