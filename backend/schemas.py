from typing import Optional, Union, Any

from fastapi.exceptions import HTTPException
from pydantic import BaseModel, validator, EmailStr, root_validator


class CreateUser(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    password: str

    class Config:
        orm_mode = True


class ViewCreatedUser(BaseModel):
    email: str
    id: int
    username: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class ViewUser(BaseModel):
    email: str
    id: int
    username: str
    first_name: str
    last_name: str
    is_subscribed: bool

    class Config:
        orm_mode = True


class CurrentUser(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    id: int

    class Config:
        orm_mode = True


class SetPassword(BaseModel):
    new_password: str
    current_password: str

    class Config:
        orm_mode = True


# class PostTags(BaseModel):
#     id: int

#     class Config:
#         orm_mode = True


class PostIngredients(BaseModel):
    id: int
    amount: int

    class Config:
        orm_mode = True


class PostRecipes(BaseModel):
    ingredients: list[PostIngredients]
    tags: list[int]
    image: Optional[str]
    name: str
    text: str
    cooking_time: int

    class Config:
        orm_mode = True

    @validator('ingredients', pre=True, always=True)
    def validate_ingredients(cls, data):
        if data is not None and data != '' and data != []:
            return data
        raise HTTPException(status_code=400, detail='Ingredients are required')
    
    @validator('tags', pre=True, always=True)
    def validate_tags(cls, data):
        if data is not None and data != '' and data != []:
            return data
        raise HTTPException(status_code=400, detail='Tags are required')

    @validator('image', pre=True, always=True)
    def validate_image(cls, data):
        if data is not None and data != '':
            return data
        raise HTTPException(status_code=400, detail='Image is required')

    @validator('name', pre=True, always=True)
    def validate_name(cls, data):
        if data is not None and data != '':
            return data
        raise HTTPException(status_code=400, detail='Name is required')
    
    @validator('text', pre=True, always=True)
    def validate_text(cls, data):
        if data is not None and data != '':
            return data
        raise HTTPException(status_code=400, detail='Text is required')
         
    @validator('cooking_time', pre=True, always=True, allow_reuse=True)
    def validate_cooking_time(cls, data):
        if data is not None and data != '':
            return data
        raise HTTPException(status_code=400, detail='Cooking time is required')


class CreateToken(BaseModel):
    password: str
    email: str


class ViewTags(BaseModel):
    id: int
    name: str
    color: str
    slug: str

    class Config:
        orm_mode =True


class ViewIngredients(BaseModel):
    id: int
    name: str
    measurement_unit: str
    amount: int

    class Config:
        orm_mode = True


class ViewRecipes(BaseModel):
    id: int
    tags: list[ViewTags]
    author: ViewUser
    ingredients: list[ViewIngredients]
    name: str
    image: Optional[str] = None
    text: str
    cooking_time: int
    is_favorited: bool
    is_in_shopping_cart: bool

    class Config:
        orm_mode = True


class ShortRecipe(BaseModel):
    id: int
    name: str
    image: Optional[str] = None
    cooking_time: int

    class Config:
        orm_mode = True


class SubscribeUser(BaseModel):
    email: str
    id: int
    username: str
    first_name: str
    last_name: str
    is_subscribed: bool
    recipes: list[ShortRecipe]
    recipe_count: int

    class Config:
        orm_mode = True
