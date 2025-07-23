import os
from .base import Base
from .session import get_db

from dotenv import load_dotenv

load_dotenv()  # .env file se environment variables load karega

class Settings:
    PROJECT_NAME = "Daily Parwan"
    DATABASE_URL = os.getenv("DATABASE_URL")

settings = Settings()
