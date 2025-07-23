from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.admin_user import AdminUserCreate, AdminUserOut
from app.models.admin_user import AdminUser
from app.core.security import hash_password
from app.db.session import get_db

router = APIRouter()

@router.post("/admin/register", response_model=AdminUserOut)
def register_admin(user: AdminUserCreate, db: Session = Depends(get_db)):
    if db.query(AdminUser).filter(AdminUser.email == user.email).first():
        raise HTTPException(status_code=400, detail="ای میل پہلے سے رجسٹرڈ ہے")

    new_user = AdminUser(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
        role="admin"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
