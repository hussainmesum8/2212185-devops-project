import os
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://devops_user:devops_pass@db:5432/devops_db"
)

engine = engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Export text() so main.py can use it for the health check
__all__ = ["engine", "SessionLocal", "Base", "text"]
