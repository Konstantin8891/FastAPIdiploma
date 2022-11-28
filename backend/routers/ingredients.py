from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .auth import get_db

import sys
sys.path.append('..')

from models import Ingredient

router = APIRouter(prefix='/api/ingredients', tags=['ingredients'])


@router.get('/')
async def get_all_ingredients(
    name: Optional[str] = None, db: Session = Depends(get_db)
):
    if name:
        return db.query(Ingredient).filter(Ingredient.name.startswith(name)).all()
    return db.query(Ingredient).all()


@router.get('/{tag_id}/')
async def get_ingredient_by_id(tag_id: int, db: Session = Depends(get_db)):
    ingredient = db.query(Ingredient).get(tag_id)
    if ingredient is None:
        raise HTTPException(status_code=400, detail='ingredient does not exist')
    return ingredient
