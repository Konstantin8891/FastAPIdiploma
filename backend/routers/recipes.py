import base64
import json
import shutil

from datetime import datetime

from fastapi import APIRouter, Depends, status, File
from sqlalchemy.orm import Session

from .auth import get_db

import sys
sys.path.append('..')

from schemas import PostRecipes

import models


router = APIRouter(prefix='/api/recipes', tags=['recipes'])


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_recipe(recipe: PostRecipes, db: Session = Depends(get_db)):
    recipe_model = models.Recipe()
    recipe_model.text = recipe.text
    # recipe_model.image = recipe.image
    file_location = f'media/{recipe.name}'
    with open(file_location, 'wb+') as image:
        # shutil.copyfileobj(recipe.image, image)
        image.write(base64.decodebytes(recipe.image))
    recipe.image = f'http://localhost:8000/media/{recipe_model.name}'
    recipe_model.name = recipe.name
    recipe_model.cooking_time = recipe.cooking_time
    recipe_model.created = datetime.now()
    recipe_model.author_id = 1
    db.add(recipe_model)
    db.commit()
    db.refresh(recipe_model)
    for tag in recipe.tags:
        tag_model = db.query(models.Tag).get(tag.id)
        recipe_model.tags.append(tag_model)
    db.commit()
    for ingredient in recipe.ingredients:
        ingredient_model = db.query(models.Ingredient).get(ingredient.id)
        recipe_model.ingredients.append(ingredient_model)
        db.commit()
        ingredient_amount = models.IngredientAmount()
        ingredient_amount.ingredient_id = ingredient.id
        ingredient_amount.amount = ingredient.amount
        db.add(ingredient_amount)
        db.commit()
    return recipe