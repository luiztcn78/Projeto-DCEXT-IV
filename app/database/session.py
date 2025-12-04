# app/database/session.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Use a URL completa do .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Se ainda não estiver definida, use esta:
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:ahdifhavajxb@db.evxthciabgwbqsvtzclw.supabase.co:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()