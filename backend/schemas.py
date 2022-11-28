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



class PostTags(BaseModel):
    id: int

    class Config:
        orm_mode = True


class PostIngredients(BaseModel):
    id: int
    amount: int

    class Config:
        orm_mode = True


class PostRecipes(BaseModel):
    ingredients: list[PostIngredients]
    tags: list[PostTags]
    # image: bytes
    image: str
    name: str
    text: str
    cooking_time: int

    class Config:
        orm_mode = True

class CreateToken(BaseModel):
    password: str
    email: str
