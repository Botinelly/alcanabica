from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()