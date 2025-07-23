# src/app/db/base.py

from sqlalchemy.orm import declarative_base

Base = declarative_base()
pass
# Base class for all models
# This will be used to create the database tables and map the models to the database