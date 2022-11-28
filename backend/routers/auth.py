from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from routers.services.authenticate import authenticate_user

import sys
sys.path.append('..')

import models

from database import SessionLocal
from schemas import CreateToken


SECRET_KEY = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix='/api/auth', tags=['auth'])


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        email: str = payload.get("sub")
        user_id: int = payload.get("id")
        if email is None or user_id is None:
            raise HTTPException(status_code=401, detail='User not found')
        return {"email": email, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=404, detail='User not found')


@router.post('/token/login/')
async def get_token(credentials: CreateToken, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if user is None:
        raise HTTPException(status_code=400, detail='User not found')
    authenticate_user(user.username, credentials.password, db)
    encode = {"sub": credentials.email, "id": user.id}
    expire = datetime.utcnow() + timedelta(minutes=60)
    encode.update({"exp": expire})
    return {"auth_token": jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)}
