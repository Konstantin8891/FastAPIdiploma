from pydantic import BaseModel


class Users(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str

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
    image: str
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
    author: CurrentUser
    ingredients: list[ViewIngredients]
    name: str
    image: str
    text: str
    cooking_time: int
    is_favorited: bool

    class Config:
        orm_mode = True


class ShortRecipe(BaseModel):
    id: int
    name: str
    image: str
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
