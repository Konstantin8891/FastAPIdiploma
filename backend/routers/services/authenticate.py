from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from routers.services.password import verify_password

import sys
sys.path.append('...')

from models import User


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=400, detail='User not found')
    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail='Wrong password')
    return user