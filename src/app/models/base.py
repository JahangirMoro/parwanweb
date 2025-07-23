# src/app/models/base.py
from app.models.edition import Edition
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
