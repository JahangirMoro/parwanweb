from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/admin/dashboard", response_class=HTMLResponse)
def admin_dashboard(request: Request):
    admin_user_id = request.cookies.get("admin_user")
    if not admin_user_id:
        raise HTTPException(status_code=401, detail="لاگ ان ضروری ہے")

    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request
    })
