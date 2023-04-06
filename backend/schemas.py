from typing import Optional, Union, Any

from pydantic import BaseModel


class CreateUser(BaseModel):
    email: str
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
    image: Optional[str]
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
