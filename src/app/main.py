import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# -------------------------------
# 🧩 Backend APIs (CRUD etc.)
# -------------------------------
from app.api import news
from app.api import image_upload
from app.api import category

# -------------------------------
# 🧩 Admin side API routes
# -------------------------------
from app.api.routes import admin
from app.api.routes import frontend
from app.api.routes import categories
from app.api.routes.editions import router as edition_router

# -------------------------------
# 🧩 Web (Jinja2) - User & Admin
# -------------------------------
from app.api.web import home
from app.api.web import category as web_category
from app.api.web import news_detail
from app.api.web import news as web_news
from app.api.web import search
from app.api.web import contact
from app.api.web.archive import router as archive_router
from app.api.web import admin_dashboard
from app.api.web import admin_auth
from app.api.web import epaper as epaper_web

# ✅ Create FastAPI app
app = FastAPI()

# ✅ Absolute directories
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))         # src/app
BASE_DIR = os.path.dirname(CURRENT_DIR)                          # src
STATIC_DIR = os.path.join(CURRENT_DIR, "static")                 # src/app/static
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")                  # src/uploads
TEMPLATES_DIR = os.path.join(CURRENT_DIR, "templates")           # ✅ src/app/templates

# ✅ Static Files
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
else:
    print(f"⚠️ Static dir not found: {STATIC_DIR}")

if os.path.isdir(UPLOADS_DIR):
    app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
else:
    print(f"⚠️ Uploads dir not found: {UPLOADS_DIR}")

# ✅ Inject global Jinja2 templates
if os.path.isdir(TEMPLATES_DIR):
    app.state.templates = Jinja2Templates(directory=TEMPLATES_DIR)
else:
    print(f"❌ Templates dir not found: {TEMPLATES_DIR}")

# ✅ Routers
app.include_router(edition_router)
app.include_router(categories.router)
app.include_router(admin.router)
app.include_router(image_upload.router, tags=["Upload"])
app.include_router(news.router, prefix="/news", tags=["News"])
app.include_router(category.router, prefix="/categories", tags=["Categories"])

# Admin
app.include_router(admin_auth.router)
app.include_router(admin_dashboard.router)

# Web
app.include_router(home.router)
app.include_router(web_category.router)
app.include_router(news_detail.router)
app.include_router(web_news.router)
app.include_router(search.router)
app.include_router(contact.router)
app.include_router(archive_router)
app.include_router(epaper_web.router)
app.include_router(frontend.router)

# ✅ Uvicorn Entrypoint (for Render)
def main():
    import uvicorn
    port = int(os.environ.get("PORT", 10000))  # Render uses this port
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
