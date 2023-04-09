from typing import Optional

from fastapi import APIRouter, status, Depends, HTTPException, Security, Request
from fastapi_pagination import add_pagination
from sqlalchemy.orm import Session

from .auth import get_user, get_db, get_user_or_none, get_user_and_hashed_token
from .services.pagination import Page, Params
from .services.hash import get_hash, verify_hash

import sys
sys.path.append('..')

import models
from serializers import UserSerializer

from schemas import (
    CreateUser,
    CurrentUser,
    SubscribeUser,
    ViewCreatedUser,
    ViewUser,
    SetPassword,
    ShortRecipe
)


# oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix='/api/users', tags=['users'])


def get_is_subscribed(user: dict, user_id: int, db: Session):
    subscriber = db.query(models.Subscriber).filter(
        models.Subscriber.author_id == user_id
    ).filter(models.Subscriber.user_id == user.get('id')).first()
    # print(subscriber)
    if subscriber is None:
        return False
    else:
        return True


@router.post(
    '/', status_code=status.HTTP_201_CREATED, response_model=ViewCreatedUser
)
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    user_model = models.User()
    if user.email == '':
        raise HTTPException(status_code=400, detail='Email is required')
    if user.username == '':
        raise HTTPException(status_code=400, detail='Username is required')
    if user.first_name == '':
        raise HTTPException(status_code=400, detail='First name is required')
    if user.last_name == '':
        raise HTTPException(status_code=400, detail='Last name is required')
    if user.password == '':
        raise HTTPException(status_code=400, detail='Password is required')
    user_model.email = user.email
    user_model.username = user.username
    user_model.first_name = user.first_name
    user_model.last_name = user.last_name
    user_model.password = get_hash(user.password)
    user_model.role = 'user'
    db.add(user_model)
    db.commit()
    db.refresh(user_model)
    return user_model


@router.get('/')
async def get_all_users(
    page: int,
    limit: int,
    request: Request,
    user: Optional[dict] = Security(get_user_or_none),
    db: Session = Depends(get_db)
):
    if user is not None:
        _, token_hashed = get_user_and_hashed_token(db, user)
    else:
        token_hashed = None
    if not (token_hashed and verify_hash(user.get('token'), token_hashed)):
        user = None
    users = db.query(models.User).order_by(models.User.id).all()[
        ((page - 1) * limit):(page * limit)
    ]
    count = db.query(models.User).count()
    if (count % limit != 0 and count // limit + 1 < page) or (
        count % limit == 0 and count / limit < page
    ):
        raise HTTPException(status_code=400, detail='Page does not exist')
    if (count % limit != 0 and count // limit + 1 == page) or (
        count % limit == 0 and count / limit == page
    ):
        next = None
    else:
        next = f'http://{request.client.host}:{request.url.port}/?page={page + 1}'
    if page == 1:
        prev = None
    else:
        prev = f'http://{request.client.host}:{request.url.port}/?page={page - 1}'
    result = {}
    result['count'] = count
    result['next'] = next
    result['previous'] = prev
    result['results'] = []
    for user_instance in users:
        sub_res = {}
        sub_res['email'] = user_instance.email
        sub_res['id'] = user_instance.id
        sub_res['username'] = user_instance.username
        sub_res['first_name'] = user_instance.first_name
        sub_res['last_name'] = user_instance.last_name
        sub_res['role'] = user_instance.role
        if user is None:
            sub_res['is_subscribed'] = False
        else:
            sub_res['is_subscribed'] = get_is_subscribed(user, user_instance.id, db)
            # subscription = db.query(models.Subscriber).filter(
            #     models.Subscriber.user_id == user.get('id')
            # ).filter(models.Subscriber.author_id == user_instance.id).first()
            # if subscription is None:
            #     sub_res['is_subscribed'] = False
            # else:
            #     sub_res['is_subscribed'] = True
        result['results'].append(sub_res)
    return result


@router.get('/me/', response_model=ViewUser)
async def get_current_user(
    user: dict = Security(get_user), db: Session = Depends(get_db)
):
    user_model, token_hashed = get_user_and_hashed_token(db, user)
    if token_hashed and verify_hash(user.get('token'), token_hashed):
        # user_model = db.query(models.User).get(user.get('id'))
        is_subscribed = get_is_subscribed(user, user.get('id'), db)
        return ViewUser(
            email=user_model.email,
            id=user_model.id,
            username=user_model.username,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            is_subscribed=is_subscribed
        )
    raise HTTPException(status_code=403, detail='Unauthorized')


@router.get('/subscriptions/')
async def get_all_subscriptions(
    page: int,
    limit: int,
    request: Request,
    recipe_limit: Optional[int] = None,
    user: dict = Security(get_user),
    db: Session = Depends(get_db)
):
    _, token_hashed = get_user_and_hashed_token(db, user)
    if token_hashed and verify_hash(user.get('token'), token_hashed):
        authors = db.query(models.Subscriber).filter(
            models.Subscriber.user_id == user.get('id')
        ).order_by(models.Subscriber.author_id).all()[
            ((page - 1) * limit):(page * limit)
        ]
        count = db.query(models.Subscriber).filter(models.Subscriber.user_id == user.get('id')).count()
        if (count % limit != 0 and count // limit + 1 < page) or (
            count % limit == 0 and count / limit < page
        ):
            raise HTTPException(status_code=400, detail='Page does not exist')
        if (count % limit != 0 and count // limit + 1 == page) or (
            count % limit == 0 and count / limit == page
        ):
            next = None
        else:
            next = f'http://{request.client.host}:{request.url.port}/?page={page + 1}'
        if page == 1:
            prev = None
        else:
            prev = f'http://{request.client.host}:{request.url.port}/?page={page - 1}'
        result = {}
        result['count'] = count
        result['next'] = next
        result['previous'] = prev
        result['results'] = []
        for author in authors:
            user_instance = db.query(models.User).get(author.author_id)
            sub_res = {}
            sub_res['email'] = user_instance.email
            sub_res['id'] = user_instance.id
            sub_res['username'] = user_instance.username
            sub_res['first_name'] = user_instance.first_name
            sub_res['last_name'] = user_instance.last_name
            sub_res['is_subscribed'] = True
            recipes = db.query(models.Recipe).filter(
                models.Recipe.author_id == author.author_id
            ).order_by(models.Recipe.id)
            if recipe_limit:
                recipes = recipes[:recipe_limit]
            sub_res['recipes'] = []
            for recipe in recipes:
                if recipe.image_id:
                    image = db.query(models.Image).get(recipe.image_id)
                    recipe_instance = ShortRecipe(
                        id=recipe.id,
                        name=recipe.name,
                        image=image.url,
                        cooking_time=recipe.cooking_time
                    )
                else:
                    recipe_instance = ShortRecipe(
                        id=recipe.id,
                        name=recipe.name,
                        cooking_time=recipe.cooking_time
                    )

                sub_res['recipes'].append(recipe_instance)
            result['results'].append(sub_res)
        return result
    raise HTTPException(status_code=403, detail='Unauthorized')


@router.get('/{user_id}/', response_model=ViewUser)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    user: dict = Security(get_user)
):
    _, token_hashed = get_user_and_hashed_token(db, user)
    if token_hashed and verify_hash(user.get('token'), token_hashed):
        user_model = db.query(models.User).filter(models.User.id == user_id).first()
        if user_model is None:
            raise HTTPException(status_code=400, detail='User does not exist')
        is_subscribed = get_is_subscribed(user, user_id, db)
        return ViewUser(
            email=user_model.email,
            id=user_model.id,
            username=user_model.username,
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            is_subscribed=is_subscribed
        )
    raise HTTPException(status_code=403, detail='Unauthorized')


@router.post('/set_password/', status_code=status.HTTP_204_NO_CONTENT)
async def set_new_password(
    passwords: SetPassword,
    user: dict = Security(get_user),
    db: Session = Depends(get_db)
):
    user_model, token_hashed = get_user_and_hashed_token(db, user)
    if token_hashed and verify_hash(user.get('token'), token_hashed):
        user_model = db.query(models.User).get(user.get('id'))
        if verify_hash(passwords.current_password, user_model.password):
            user_model.password = get_hash(passwords.new_password)
            db.commit()
            return 'changed'
        raise HTTPException(status_code=400, detail='Check correctness of the data')
    raise HTTPException(status_code=401, detail='Unauthorized')


@router.post('/{author_id}/subscribe/', response_model=SubscribeUser)
async def get_subscribed(
    author_id: int,
    recipe_limit: Optional[int] = None,
    user: dict = Security(get_user),
    db: Session = Depends(get_db)
):
    _, token_hashed = get_user_and_hashed_token(db, user)
    if token_hashed and verify_hash(user.get('token'), token_hashed):
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
        if recipe_limit:
            recipes = db.query(models.Recipe).filter(
                models.Recipe.author_id == author_id
            )[:recipe_limit]
        else:
            recipes = db.query(models.Recipe).filter(
                models.Recipe.author_id == author_id
            )
        recipe_count = db.query(models.Recipe).filter(
            models.Recipe.author_id == author_id
        ).count()
        recipes = recipes.all()
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
    raise HTTPException(status_code=401, detail='Unauthorized')


@router.delete(
    '/{author_id}/subscribe/', status_code=status.HTTP_204_NO_CONTENT
)
async def unsubscribe(    
    author_id: int,
    user: dict = Security(get_user),
    db: Session = Depends(get_db)
):
    _, token_hashed = get_user_and_hashed_token(db, user)
    if token_hashed and verify_hash(user.get('token'), token_hashed):
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
    raise HTTPException(status_code=403, detail='Unauthorized')
