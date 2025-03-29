import random
from src.models.user import User
from sqlalchemy.orm import Session
from src.utils.email import send_email
from datetime import datetime, timedelta
from src.models.verification import VerificationCode

def generate_code():
    return f"{random.randint(100000, 999999)}"

def create_and_send_code(db: Session, email: str):
    code = generate_code()

    user = db.query(User).filter(User.email == email).first()
    if not user:
        return 000000

    db_code = VerificationCode(email=email, code=code)
    db.add(db_code)
    db.commit()

    send_email(to_email=email, subject="Código de Verificação", body=f"Seu código é: {code}")
    return code

def validate_code(db: Session, email: str, code: str):
    expiration_minutes = 10
    valid_from = datetime.utcnow() - timedelta(minutes=expiration_minutes)

    db_code = (
        db.query(VerificationCode)
        .filter(
            VerificationCode.email == email,
            VerificationCode.code == code,
            VerificationCode.created_at >= valid_from
        )
        .order_by(VerificationCode.created_at.desc())
        .first()
    )

    if db_code:
        db.delete(db_code)
        db.commit()
        return True

    return False


def clean_expired_codes(db: Session):
    threshold = datetime.utcnow() - timedelta(minutes=10)
    db.query(VerificationCode).filter(VerificationCode.created_at < threshold).delete()
    db.commit()
