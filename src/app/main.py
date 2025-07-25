from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# 🧩 Backend APIs
from app.api import news
from app.api import image_upload
from app.api import category

# 🧩 Admin side routes
from app.api.routes import admin
from app.api.routes import categories
from app.api.routes.editions import router as edition_router

# 🧩 Web frontend (Jinja2 templates)
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

# 🔗 Include routers

# ✨ Admin & Backend APIs
app.include_router(edition_router)
app.include_router(categories.router)
app.include_router(admin.router)
app.include_router(image_upload.router, tags=["Upload"])
app.include_router(news.router, prefix="/news", tags=["News"])
app.include_router(category.router, prefix="/categories", tags=["Categories"])

# 🔐 Admin Auth
app.include_router(admin_auth.router)
app.include_router(admin_dashboard.router)

# 🌐 Frontend (Jinja2)
app.include_router(home.router)
app.include_router(web_category.router)
app.include_router(news_detail.router)
app.include_router(web_news.router)
app.include_router(search.router)
app.include_router(contact.router)
app.include_router(archive_router)
app.include_router(epaper_web.router)

# 📂 Static file mounts

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ✅ Only for local development (Render will not use this)
def main():
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

# 🧪 Optional run for local testing
if __name__ == "__main__":
    main()
