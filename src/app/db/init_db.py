# src/app/db/init_db.py

from app.db.database import engine, Base
from app.models import news
#from app.models import user
from app.models import category
#from app.models import epaper
from app.models import contact
from app.models import edition
from app.models import topbar
from app.models import admin_user
from app.models.news import NewsArticle

def init_db():
    print("📦 Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully.")
    print("Registered tables:", Base.metadata.tables.keys())

if __name__ == "__main__":
    init_db()
