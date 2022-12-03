from sqlalchemy import Integer, String, Boolean, ForeignKey, Column, DateTime, LargeBinary
from sqlalchemy.schema import Table
from sqlalchemy.orm import relationship

from database import Base
from proxy_model import URLType


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)

    recipeuser = relationship('Recipe', back_populates='author')
    favorites = relationship('Favorite', back_populates='user_f')
    shoppingcart_u = relationship('ShoppingCart', back_populates='user_sc')
    # subscriber_u = relationship('Subscriber', back_populates='user_s')
    # subscriber_a = relationship('Subscriber', back_populates='user_a')


IngredientRecipeRelation = Table(
    'ingredient_recipe_relation',
    Base.metadata,
    Column('ingredient_id', Integer, ForeignKey('ingredient.id')),
    Column('recipe_id', Integer, ForeignKey('recipe.id'))
)

TagRecipeRelation = Table(
    'tag_recipe_relation',
    Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.id')),
    Column('recipe_id', Integer, ForeignKey('recipe.id'))
)

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    color = Column(String)
    slug = Column(String)

    recipes = relationship(
        'Recipe',
        secondary=TagRecipeRelation,
        back_populates='tags',
        cascade='all, delete'
    )



class Ingredient(Base):
    __tablename__ = 'ingredient'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    measurement_unit = Column(String)

    recipes = relationship(
        'Recipe',
        secondary=IngredientRecipeRelation,
        back_populates='ingredients',
        cascade='all, delete'
    )

    ingredient_amount = relationship('IngredientAmount', back_populates='ingredient')


class IngredientAmount(Base):
    __tablename__ = 'ingredient_amount'
    id = Column(Integer, primary_key=True, index=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'))
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    amount = Column(Integer)

    ingredient = relationship('Ingredient', back_populates='ingredient_amount')


class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    cooking_time = Column(Integer)
    image = Column(URLType)
    created = Column(DateTime)
    name = Column(String, unique=True)
    author_id = Column(Integer, ForeignKey('user.id'))
    ingredients = relationship(
        'Ingredient',
        secondary=IngredientRecipeRelation,
        back_populates='recipes',
        cascade='all, delete'
    )
    tags = relationship(
        'Tag',
        secondary=TagRecipeRelation,
        back_populates='recipes',
        cascade='all, delete'
    )

    author = relationship('User', back_populates='recipeuser')
    favorites_r = relationship('Favorite', back_populates='recipe_f')
    shoppingcart_r = relationship('ShoppingCart', back_populates='recipe_sc')


class Favorite(Base):
    __tablename__ = 'favorite'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    recipe_id = Column(Integer, ForeignKey('recipe.id'))

    user_f = relationship('User', back_populates='favorites')
    recipe_f = relationship('Recipe', back_populates='favorites_r')


class ShoppingCart(Base):
    __tablename__ = 'shopping_cart'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    recipe_id = Column(Integer, ForeignKey('recipe.id'))

    user_sc = relationship('User', back_populates='shoppingcart_u')
    recipe_sc = relationship('Recipe', back_populates='shoppingcart_r')


# class Subscriber(Base):
#     __tablename__ = 'subscription'
#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('user.id'))
#     author_id = Column(Integer, ForeignKey('user.id'))

#     user_s = relationship('User', back_populates='subscriber_u', foreign_keys=user_id)
#     author_s = relationship('User', back_populates='subscriber_a', foreign_keys=author_id)
