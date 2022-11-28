from fastapi import APIRouter, status, Depends, HTTPException
# from fastapi.security import OAuth2PasswordBearer
from fastapi_pagination import add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from routers.auth import get_user, get_db
from routers.services.pagination import Page
from routers.services.password import get_password_hash

import sys
sys.path.append('..')

import models

# from database import SessionLocal
from schemas import Users, CurrentUser


# oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix='/api/users', tags=['users'])


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(user: Users, db: Session = Depends(get_db)):
    user_model = models.User()
    user_model.email = user.email
    user_model.username = user.username
    user_model.first_name = user.first_name
    user_model.last_name = user.last_name
    user_model.password = get_password_hash(user.password)
    db.add(user_model)
    db.commit()
    return user


@router.get('/', response_model=Page[Users])
async def get_all_users(db: Session = Depends(get_db)):
    return paginate(db.query(models.User).order_by(models.User.id))


@router.get('/{user_id}/')
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=400, detail='User does not exist')
    return user


@router.get('/me/')
async def get_current_user(user: dict = Depends(get_user), db: Session = Depends(get_db)):
    user_model = db.query(models.User).get(user.get('id'))
    print(user_model)
    return user_model
