import base64
import io
import json
import shutil

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, status, Security, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import delete
from sqlalchemy.orm import Session, selectinload

from .auth import get_db, get_user, get_user_or_none
from routers.services.pagination import Page, Params
from routers.users import get_is_subscribed

import sys
sys.path.append('..')

from schemas import PostRecipes, ViewRecipes, ShortRecipe, ViewUser, ViewRecipes1

import models


router = APIRouter(prefix='/api/recipes', tags=['recipes'])


def build_ingredients(ingredients: dict, db: Session, recipe_instance: dict):
    ingredient_amount = []
    for ingredient in ingredients:
        ingredient_instance = db.query(models.Ingredient).filter(
            models.Ingredient.id == ingredient.ingredient_id
        ).first()
        ingredient_amount.append({
            "id": ingredient_instance.id,
            "name": ingredient_instance.name,
            "measurement_unit": ingredient_instance.measurement_unit,
            "amount": ingredient.amount
        })
    return ingredient_amount


def get_favorites(
    recipe_id: int, user: dict, db: Session = Depends(get_db)
):
    favorite = db.query(models.Favorite).filter(
        models.Favorite.recipe_id == recipe_id
    ).filter(models.Favorite.user_id == user.get('id')).first()
    if favorite is None:
        return False
    else:
        return True


def build_shopping_cart(user: dict, recipe_id: int, db: Session):
    shopping_cart = db.query(models.ShoppingCart).filter(
        models.ShoppingCart.user_id == user.get('id')
    ).filter(models.ShoppingCart.recipe_id == recipe_id).first()
    if shopping_cart is None:
        return False
    else:
        return True


def get_image_url(str_image: str, name: str, request: Request):
    format, imgstr = str_image.split(';base64,')
    ext = format.split('/')[-1]
    data = base64.b64decode(imgstr)
    file_location = f'media/recipes/images/{name}.{ext}'
    with open(file_location, 'wb+') as image:
        image.write(data)
    return (
        f'http://{request.client.host}:{request.url.port}/media/recipes/'
        f'images/{name}.{ext}'
    )
    # return (
    #     f'{request.url}images/{name}.{ext}'
    # )


@router.get('/download_shopping_cart/')
async def get_shopping_cart(
    user: dict = Security(get_user), db: Session = Depends(get_db)
):
    shopping_list = []
    instances = db.query(models.ShoppingCart).filter(
        models.ShoppingCart.user_id == user.get('id')
    )
    for instance in instances:
        recipe = db.query(models.Recipe).get(instance.recipe_id)
        ingredients_amount = db.query(models.IngredientAmount).filter(
            models.IngredientAmount.recipe_id == instance.recipe_id
        )
        for ingredient_amount in ingredients_amount:
            ingredient = db.query(models.Ingredient).get(
                ingredient_amount.ingredient_id
            )
            shopping_list.append(
                f"{recipe.name}: {ingredient.name}"
                f" - {ingredient_amount.amount}\n"
            )            
        f = open("shopping_cart.txt", "w")
        for shopping in shopping_list:
            f.write(shopping)
        f.close()
        return FileResponse('shopping_cart.txt')


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_recipe(
    recipe: PostRecipes,
    request: Request,
    user: dict = Security(get_user),
    db: Session = Depends(get_db)
):
    recipe_model = models.Recipe() #  источники данных
    recipe_model.text = recipe.text
    recipe.image = get_image_url(recipe.image, recipe.name, request)
    recipe_model.image = recipe.image
    recipe_model.name = recipe.name
    recipe_model.cooking_time = recipe.cooking_time
    recipe_model.created = datetime.now()
    recipe_model.author_id = user.get('id')
    db.add(recipe_model)
    db.commit()
    db.refresh(recipe_model)
    for tag in recipe.tags:
        tag_model = db.query(models.Tag).get(tag)
        recipe_model.tags.append(tag_model)
    db.commit() # конец
    for ingredient in recipe.ingredients: 
        ingredient_amount = models.IngredientAmount()
        ingredient_amount.ingredient_id = ingredient.id
        ingredient_amount.recipe_id = recipe_model.id
        ingredient_amount.amount = ingredient.amount
        db.add(ingredient_amount)
        db.commit()
        db.refresh(ingredient_amount)
        recipe_model.ingredients.append(ingredient_amount)
        db.commit()
    author_instance = db.query(models.User).get(user.get('id'))
    is_subscribed = get_is_subscribed(user, db) # бизнес-логика + репо
    author = ViewUser(
        email=author_instance.email,
        id=author_instance.id,
        username=author_instance.username,
        first_name=author_instance.first_name,
        last_name=author_instance.last_name,
        is_subscribed=is_subscribed
    ) # entity + dto + бизнес-логика
    ingredient_amount = build_ingredients(recipe_model.ingredients, db, recipe_model)
    recipe_view_instance = ViewRecipes(
        id=recipe_model.id,
        tags=recipe_model.tags,
        ingredients=ingredient_amount,
        author=author,
        name=recipe.name,
        image=recipe.image,
        text=recipe.text,
        cooking_time=recipe.cooking_time,
        is_favorited=False,
        is_in_shopping_cart=False
    )
    return recipe_view_instance


@router.get(
    '/', response_model=Page[ViewRecipes1], dependencies=[Depends(Params)]
    # '/', response_model=ViewRecipes1
    # '/'
)
async def get_all_recipes(db: Session = Depends(get_db)):
    # return paginate(
    #     db.query(models.Recipe).order_by(models.Recipe.id).join(
    #         models.Recipe.tags
    #     ).join(models.Recipe.ingredients).join(
    #         models.IngredientAmount.ingredient
    #     )
    # )
    return paginate(
        db.query(models.Recipe).order_by(models.Recipe.id).options(
            selectinload(models.Recipe.tags)
        ).options(
            selectinload(models.Recipe.ingredients).options(selectinload(
                models.IngredientAmount.ingredient
            ))
        )
    )



@router.get('/{recipe_id}/', response_model=ViewRecipes)
async def get_recipe_by_id(
    recipe_id: int,
    db: Session = Depends(get_db),
    user: dict = Security(get_user_or_none)
):
    recipe_instance = db.query(models.Recipe).get(recipe_id)
    if recipe_instance is None:
        raise HTTPException(status_code=400, detail='recipe not found')
    author_instance = db.query(models.User).get(recipe_instance.author_id)
    if recipe_instance is None:
        raise HTTPException(status_code=400, detail='Recipe not found')
    if author_instance is None:
        raise HTTPException(status_code=400, detail='User not found')
    ingredient_amount = build_ingredients(
        recipe_instance.ingredients, db, recipe_instance
    )
    if user is None:
        is_favorited = False
    else:
        is_favorited = get_favorites(recipe_id, user, db)
    if user is None:
        is_in_shopping_cart = False
    else:
        is_in_shopping_cart = build_shopping_cart(user, recipe_id, db)
    print(is_in_shopping_cart)
    is_subscribed = get_is_subscribed(user, db)
    author = ViewUser(
        email=author_instance.email,
        id=author_instance.id,
        username=author_instance.username,
        first_name=author_instance.first_name,
        last_name=author_instance.last_name,
        is_subscribed=is_subscribed
    )
    recipe = ViewRecipes(
        id=recipe_id,
        tags=recipe_instance.tags,
        author=author,
        ingredients=ingredient_amount,
        name=recipe_instance.name,
        image=recipe_instance.image,
        text=recipe_instance.text,
        cooking_time=recipe_instance.cooking_time,
        is_favorited=is_favorited,
        is_in_shopping_cart=is_in_shopping_cart
    )
    return recipe


@router.patch('/{recipe_id}/', response_model=ViewRecipes)
async def patch_recipe(
    recipe_id: int,
    recipe: PostRecipes,
    request: Request,
    db: Session = Depends(get_db),
    user: dict = Security(get_user)
):
    recipe_instance = db.query(models.Recipe).get(recipe_id)
    if recipe_instance.author_id != user.get('id'):
        raise HTTPException(
            status_code=403, detail='You have no rights to edit this recipe'
        )
    recipe_instance.image = get_image_url(recipe.image, recipe.name, request)
    recipe_instance.name = recipe.name
    recipe_instance.text = recipe.text
    recipe_instance.cooking_time = recipe.cooking_time
    recipe_instance.ingredients = []
    for ingredient in recipe.ingredients:
        ingredient_amount_instance = models.IngredientAmount()
        ingredient_amount_instance.ingredient_id = ingredient.id
        ingredient_amount_instance.recipe_id = recipe_id
        ingredient_amount_instance.amount = ingredient.amount
        db.add(ingredient_amount_instance)
        db.commit()
        db.refresh(ingredient_amount_instance)
        recipe_instance.ingredients.append(ingredient_amount_instance)
        db.commit()        
    recipe_instance.tags = []
    for tag in recipe.tags:
        tag_model = db.query(models.Tag).get(tag)
        recipe_instance.tags.append(tag_model)
    db.commit()
    ingredient_amount = build_ingredients(
        recipe_instance.ingredients, db, recipe_instance
    )
    author_instance = db.query(models.User).get(user.get('id'))

    is_favorited = get_favorites(recipe_id, user, db)
    is_subscribed = get_is_subscribed(user, db)
    author = ViewUser(
        email=author_instance.email,
        id=author_instance.id,
        username=author_instance.username,
        first_name=author_instance.first_name,
        last_name=author_instance.last_name,
        is_subscribed=is_subscribed
    )
    is_in_shopping_cart = build_shopping_cart(user, recipe_id, db)
    recipe = ViewRecipes(
        id=recipe_id,
        tags=recipe_instance.tags,
        ingredients=ingredient_amount,
        author=author,
        name=recipe_instance.name,
        image=recipe_instance.image,
        text=recipe_instance.text,
        cooking_time=recipe_instance.cooking_time,
        is_favorited=is_favorited,
        is_in_shopping_cart=is_in_shopping_cart
    )
    return recipe


@router.delete('/{recipe_id}/', status_code=204)
async def delete_recipe(
    recipe_id: int,
    user: dict = Security(get_user),
    db: Session = Depends(get_db)
):
    author_instance = db.query(models.User).get(user.get('id'))
    recipe_instance = db.query(models.Recipe).get(recipe_id)
    if recipe_instance is None:
        raise HTTPException(status_code=400, detail='Recipe does not exist')
    if user.get('id') != recipe_instance.author_id:
        raise HTTPException(
            status_code=403,
            detail='You do not havea permission to delete recipe'
        )
    db.query(models.Recipe).filter(models.Recipe.id == recipe_id).delete()
    db.commit()
    return 'deleted'


@router.post('/{recipe_id}/favorite/', status_code=201)
async def add_to_favorites(
    recipe_id: int,
    user: dict = Security(get_user),
    db: Session = Depends(get_db)
):
    recipe = db.query(models.Recipe).get(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=400, detail='recipe does not exist')
    favorite = db.query(models.Favorite).filter(
        models.Favorite.user_id == user.get('id')
    ).filter(models.Favorite.recipe_id == recipe_id).first()
    if favorite is not None:
        raise HTTPException(
            status_code=400, detail='recipe is already in favorites'
        )
    favorite_instance = models.Favorite()
    favorite_instance.user_id = user.get('id')
    favorite_instance.recipe_id = recipe_id
    db.add(favorite_instance)
    db.commit()
    recipe = ShortRecipe(
        id=recipe_id,
        name=recipe.name,
        image=recipe.image,
        cooking_time=recipe.cooking_time
    )
    return recipe

@router.delete('/{recipe_id}/favorite/', status_code=204)
async def delete_from_favorites(
    recipe_id: int,
    user: dict = Security(get_user),
    db: Session = Depends(get_db)
):
    recipe = db.query(models.Recipe).get(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=400, detail='recipe does not exist')
    favorite = db.query(models.Favorite).filter(
        models.Favorite.user_id == user.get('id')
    ).filter(models.Favorite.recipe_id == recipe_id).first()
    if favorite is None:
        raise HTTPException(
            status_code=400, detail='recipe is not in favorites'
        )
    db.query(models.Favorite).filter(
        models.Favorite.user_id == user.get('id')
    ).filter(models.Favorite.recipe_id == recipe_id).delete()
    db.commit()
    return 'deleted'


@router.post('/{recipe_id}/shopping_cart/', response_model=ShortRecipe)
async def add_to_shopping_cart(
    recipe_id: int,
    user: dict = Security(get_user),
    db: Session = Depends(get_db)
):
    recipe = db.query(models.Recipe).get(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=400, detail='recipe not found')
    shopping_cart = models.ShoppingCart()
    shopping_cart.recipe_id = recipe_id
    shopping_cart.user_id = user.get('id')
    db.add(shopping_cart)
    db.commit()
    recipe = ShortRecipe(
        id=recipe_id,
        name=recipe.name,
        image=recipe.image,
        cooking_time=recipe.cooking_time
    )
    return recipe


@router.delete('/{recipe_id}/shopping_cart/')
async def delete_from_shopping_cart(
    recipe_id: int,
    user: dict = Security(get_user),
    db: Session = Depends(get_db)
):
    recipe = db.query(models.Recipe).get(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=400, detail='recipe not found')
    favorite = db.query(models.ShoppingCart).filter(
        models.ShoppingCart.user_id == user.get('id')
    ).filter(models.ShoppingCart.recipe_id == recipe.id).first()
    if favorite is None:
        raise HTTPException(status_code=400, detail='recipe is not in favorited')
    db.query(models.ShoppingCart).filter(
        models.ShoppingCart.user_id == user.get('id')
    ).filter(models.ShoppingCart.recipe_id == recipe.id).delete()
    db.commit()
    return 'deleted'



