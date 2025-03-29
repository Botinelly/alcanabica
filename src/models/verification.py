from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from src.database.connection import Base

class VerificationCode(Base):
    __tablename__ = "verification_codes"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    code = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
