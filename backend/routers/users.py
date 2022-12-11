from fastapi import APIRouter, status, Depends, HTTPException, Security
# from fastapi.security import OAuth2PasswordBearer
from fastapi_contrib.pagination import Pagination
from fastapi_pagination import add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from routers.auth import get_user, get_db
from routers.services.pagination import Page
from routers.services.password import get_password_hash, verify_password

import sys
sys.path.append('..')

import models
from serializers import UserSerializer

# from database import SessionLocal
from schemas import (
    CreateUser,
    CurrentUser,
    SubscribeUser,
    ViewCreatedUser,
    ViewUser,
    SetPassword
)


# oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix='/api/users', tags=['users'])


def get_is_subscribed(user: dict, db: Session):
    subscriber = db.query(models.Subscriber).filter(
        models.Subscriber.author_id == user.get('id')
    ).filter(models.Subscriber.user_id == user.get('id')).first()
    if subscriber is None:
        return False
    else:
        return True


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=ViewCreatedUser
)
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    user_model = models.User()
    user_model.email = user.email
    user_model.username = user.username
    user_model.first_name = user.first_name
    user_model.last_name = user.last_name
    user_model.password = get_password_hash(user.password)
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model


@router.get('/', response_model=Page[ViewUser])
async def get_all_users(db: Session = Depends(get_db)):
    return paginate(db.query(models.User).order_by(models.User.id))
# @router.get('/')
# async def get_all_users(
#     db: Session = Depends(get_db), pagination: Pagination = Depends()
# ):
#     return await pagination.paginate(
#         serializer_class=UserSerializer(count=db.query(models.User).count())
#         # db.query(models.User).order_by(models.User.id)
#     )


@router.get('/me/', response_model=ViewUser)
async def get_current_user(
    user: dict = Security(get_user), db: Session = Depends(get_db)
):
    user_model = db.query(models.User).get(user.get('id'))

    # subscriber = db.query(models.Subscriber).filter(
    #     models.Subscriber.author_id == user.get('id')
    # ).filter(models.Subscriber.user_id == user.get('id')).first()
    # if subscriber is None:
    #     is_subscribed = False
    # else:
    #     is_subscribed = True
    is_subscribed = get_is_subscribed(user, db)
    return ViewUser(
        email=user_model.email,
        id=user_model.id,
        username=user_model.username,
        first_name=user_model.first_name,
        last_name=user_model.last_name,
        is_subscribed=is_subscribed
    )


@router.get('/{user_id}/', response_model=ViewUser)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    user: dict = Security(get_user)
):
    user_model = db.query(models.User).filter(models.User.id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=400, detail='User does not exist')
    # subscriber = db.query(models.Subscriber).filter(
    #     models.Subscriber.author_id == user_id
    # ).filter(models.Subscriber.user_id == user.get('id')).first()
    # if subscriber is None:
    #     is_subscribed = False
    # else:
    #     is_subscribed = True
    is_subscribed = get_is_subscribed(user, db)
    return ViewUser(
        email=user_model.email,
        id=user_model.id,
        username=user_model.username,
        first_name=user_model.first_name,
        last_name=user_model.last_name,
        is_subscribed=is_subscribed
    )


@router.post('/set_password/', status_code=status.HTTP_204_NO_CONTENT)
async def set_new_password(
    passwords: SetPassword,
    user: dict = Security(get_user),
    db: Session = Depends(get_db)
):
    user_model = db.query(models.User).get(user.get('id'))
    if verify_password(passwords.current_password, user_model.password):
        user_model.password = get_password_hash(passwords.new_password)
    return 'changed'



@router.post('/{author_id}/subscribe/', response_model=SubscribeUser)
async def get_subscribed(
    author_id: int,
    recipe_limit: int,
    user: dict = Security(get_user),
    db: Session = Depends(get_db)
):
    author = db.query(models.User).get(author_id)
    if author is None:
        raise HTTPException(status_code=400, detail='author does not exist')
    subscription = db.query(models.Subscriber).filter(
        models.Subscriber.author_id == author_id
    ).filter(models.Subscriber.user_id == user.get('id')).first()
    if subscription is not None:
        raise HTTPException(status_code=400, detail='already subscribed')
    subscribe = models.Subscriber()
    subscribe.author_id = author_id
    subscribe.user_id = user.get('id')
    db.add(subscribe)
    db.commit()
    recipes = db.query(models.Recipe).filter(
        models.Recipe.author_id == author_id
    )[:recipe_limit]
    recipe_count = db.query(models.Recipe).filter(
        models.Recipe.author_id == author_id
    ).count()
    user_instance = SubscribeUser(
        email=author.email,
        id=author_id,
        username=author.username,
        first_name=author.first_name,
        last_name=author.last_name,
        is_subscribed=True,
        recipes=recipes,
        recipe_count=recipe_count
    )
    return user_instance


@router.delete(
    '/{author_id}/subscribe/', status_code=status.HTTP_204_NO_CONTENT
)
async def unsubscribe(    
    author_id: int,
    user: dict = Security(get_user),
    db: Session = Depends(get_db)
):
    author = db.query(models.User).get(author_id)
    if author is None:
        raise HTTPException(status_code=400, detail='author does not exist')
    subscription = db.query(models.Subscriber).filter(
        models.Subscriber.author_id == author_id
    ).filter(models.Subscriber.user_id == user.get('id')).first()
    if subscription is None:
        raise HTTPException(status_code=400, detail="you're not subscribed")
    db.query(models.Subscriber).filter(
        models.Subscriber.author_id == author_id
    ).filter(models.Subscriber.user_id == user.get('id')).delete()
    db.commit()
    return 'deleted'


# @router.get('/subscriptions/')
# async def get_all_subscriptions(
#     user: dict = Security(get_user),
#     db: Session = Depends(get_db)
# ):
