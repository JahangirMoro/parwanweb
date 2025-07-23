# src/app/api/image_upload.py
from fastapi import APIRouter, UploadFile, File
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploads/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "url": f"/{file_path}"}
