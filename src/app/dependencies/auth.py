# src/app/dependencies/auth.py
from fastapi import Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.admin_user import AdminUser

def get_current_admin(request: Request, db: Session = Depends(get_db)) -> AdminUser:
    token = request.cookies.get("admin_token")
    if not token:
        raise HTTPException(status_code=401, detail="لاگ ان ضروری ہے")

    admin = db.query(AdminUser).filter(AdminUser.token == token).first()
    if not admin:
        raise HTTPException(status_code=401, detail="غلط یا منسوخ شدہ ٹوکن")

    return admin
