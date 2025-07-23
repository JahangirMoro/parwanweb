from app.api.web.home import router as home_router
from .category import router as category_router
from app.api.web.search import router as search_router
from fastapi import APIRouter
from app.api.web.archive import router as archive_router


router = APIRouter()
router.include_router(home_router)
router.include_router(category_router)
router.include_router(search_router)
router.include_router(archive_router)




