from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import os
from dotenv import load_dotenv

# .env load karna
load_dotenv()

# env se DB URL lena
DATABASE_URL = os.getenv("DATABASE_URL")

# engine
engine = create_engine(DATABASE_URL, echo=True)

# Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model
Base = declarative_base()

# ✅ Add this:
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
