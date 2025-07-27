from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
# ✅ Import routes
from app.api import news
from app.api import image_upload
from app.api import category

from app.api.routes import admin
from app.api.routes import categories
from app.api.routes.editions import router as edition_router

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

# ✅ Base directory is: src/app/
BASE_DIR = Path(__file__).resolve().parent

# ✅ Static path: src/app/static
STATIC_PATH = BASE_DIR / "static"

# ✅ Uploads path: Parwanweb/uploads (one level above src)
UPLOADS_PATH = BASE_DIR.parent.parent / "uploads"

# ✅ Check existence
if not STATIC_PATH.exists():
    raise RuntimeError(f"❌ Static folder not found: {STATIC_PATH}")
if not UPLOADS_PATH.exists():
    raise RuntimeError(f"❌ Uploads folder not found: {UPLOADS_PATH}")

# ✅ FastAPI app
app = FastAPI()

# ✅ Mount folders
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOADS_PATH), name="uploads")


# ✅ Include routers
app.include_router(edition_router)
app.include_router(categories.router)
app.include_router(admin.router)
app.include_router(image_upload.router, tags=["Upload"])
app.include_router(news.router, prefix="/news", tags=["News"])
app.include_router(category.router, prefix="/categories", tags=["Categories"])

app.include_router(admin_auth.router)
app.include_router(admin_dashboard.router)

app.include_router(home.router)
app.include_router(web_category.router)
app.include_router(news_detail.router)
app.include_router(web_news.router)
app.include_router(search.router)
app.include_router(contact.router)
app.include_router(archive_router)
app.include_router(epaper_web.router)

# ✅ Entry point for uvicorn
def main():
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
