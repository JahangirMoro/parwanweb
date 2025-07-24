from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# 🧩 Backend APIs (CRUD etc.)
from app.api import news
from app.api import image_upload
from app.api import category

# 🧩 Admin side API routes
from app.api.routes import admin
from app.api.routes import public
from app.api.routes import frontend
from app.api.routes import categories
from app.api.routes.editions import router  as edition_router

# 🧩 Web side (Jinja2 templates rendering) - User & Admin interface
from app.api.web import home
from app.api.web import category as web_category
from app.api.web import news_detail
from app.api.web import news as web_news
from app.api.web import search
from app.api.web import contact
from app.api.web.archive import router as archive_router
from app.api.web import admin_dashboard
from app.api.web import admin_auth
from app.api.web import epaper as epaper_web  # 📄 E-paper viewing route

# ✅ Create FastAPI app
app = FastAPI()

# 🔗 Include all routers below

# -------------------------------
# ✨ Admin Panel & Backend APIs
# -------------------------------
app.include_router(edition_router)  # Editions CRUD routes
app.include_router(categories.router)  # Categories CRUD
app.include_router(admin.router)  # Admin panel main
app.include_router(image_upload.router, tags=["Upload"])  # Image uploads
app.include_router(news.router, prefix="/news", tags=["News"])  # News API
app.include_router(category.router, prefix="/categories", tags=["Categories"])  # Category API

# -------------------------------
# 🔐 Admin Authentication
# -------------------------------
app.include_router(admin_auth.router)  # Admin login/logout
app.include_router(admin_dashboard.router)  # Admin dashboard

# -------------------------------
# 🌐 Website Frontend (Jinja2)
# -------------------------------
app.include_router(home.router)  # Homepage
app.include_router(web_category.router)  # News by category
app.include_router(news_detail.router)  # Single news article
app.include_router(web_news.router)  # News pages
app.include_router(search.router)  # Search feature
app.include_router(contact.router)  # Contact us page
app.include_router(archive_router)  # Date-wise archive
app.include_router(epaper_web.router)  # 📄 E-paper routes (like /epaper/1/today)
app.include_router(public.router)  # Misc public pages
app.include_router(frontend.router)  # Any extra frontend routes
import os
from fastapi.staticfiles import StaticFiles

# -------------------------------
# 📂 Static & Upload Files Mount
# -------------------------------
#app.mount("/static", StaticFiles(directory="src/app/static"), name="static")
#app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
#app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# 👇 Adjust this path because you're running from inside `src`
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")

app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
# -------------------------------
# 🏁 Uvicorn run (only when run via `uv run parwanmain`)
# -------------------------------
def main():
    import uvicorn
    #uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


    port = int(os.environ.get("PORT", 8000))  # Render will provide PORT env variable

    uvicorn.run("app.main:app", host="0.0.0.0", port=port)