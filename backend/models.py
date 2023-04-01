import logging

from sqlalchemy import (
    Integer, String, Boolean, ForeignKey, Column, DateTime, func, Unicode
)
from sqlalchemy_utils.types.url import URLType
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.schema import Table
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from sqlalchemy_utils import EmailType, ChoiceType

from database import Base, SessionLocal, engine
# from proxy_model import URLType


current_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine
))

ROLES = (('admin', 'admin'), ('user', 'user'))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(EmailType, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    role = Column(ChoiceType(ROLES))

    recipeuser = relationship('Recipe', back_populates='author')
    favorites = relationship('Favorite', back_populates='user_f')
    shoppingcart_u = relationship('ShoppingCart', back_populates='user_sc')

    def __str__(self):
        return self.username

    def is_admin(self):
        return self.role == 'admin'


# IngredientRecipeRelation = Table(
#     'ingredient_recipe_relation',
#     Base.metadata,
#     Column('ingredient_id', Integer, ForeignKey('ingredient_amount.id')),
#     Column('recipe_id', Integer, ForeignKey('recipe.id'))
# )

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

    def __str__(self):
        return self.name


class Ingredient(Base):
    __tablename__ = 'ingredient'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    measurement_unit = Column(String)

    ingredient_amount = relationship('IngredientAmount', back_populates='ingredient')

    def __str__(self):
        return self.name


class IngredientAmount(Base):
    __tablename__ = 'ingredient_amount'
    id = Column(Integer, primary_key=True, index=True, nullable=True)
    ingredient_id = Column(Integer, ForeignKey('ingredient.id'))
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    amount = Column(Integer)

    ingredient = relationship('Ingredient', back_populates='ingredient_amount')

    recipes = relationship(
        'Recipe',
        back_populates='ingredients',
        cascade='all, delete'
    )

    def __str__(self):
        ingredient = current_session.query(Ingredient).get(self.ingredient_id)
        return f'{ingredient} {self.amount}'


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(64))
    path = Column(Unicode(128))
    url = Column(URLType)

    recipe = relationship('Recipe', back_populates='image')

    # def __unicode__(self):
    #     return self.url

    def __str__(self):
        return self.url


class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    cooking_time = Column(Integer)
    image_id = Column(Integer, ForeignKey('image.id'), nullable=True)
    created = Column(DateTime)
    name = Column(String, unique=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    ingredients = relationship(
        'IngredientAmount',
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
    image = relationship('Image', back_populates='recipe')
    favorites_r = relationship('Favorite', back_populates='recipe_f')
    shoppingcart_r = relationship('ShoppingCart', back_populates='recipe_sc')

    @hybrid_property
    def favorites(self):
        query = current_session.query(Favorite).filter(Favorite.recipe_id == self.id)
        query = query.with_entities(func.count())
        query = query.scalar()
        return query
        


class Favorite(Base):
    __tablename__ = 'favorite'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    recipe_id = Column(Integer, ForeignKey('recipe.id'))

    user_f = relationship('User', back_populates='favorites')
    recipe_f = relationship('Recipe', back_populates='favorites_r')


class ShoppingCart(Base):
    __tablename__ = 'shopping_cart'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    recipe_id = Column(Integer, ForeignKey('recipe.id'))

    user_sc = relationship('User', back_populates='shoppingcart_u')
    recipe_sc = relationship('Recipe', back_populates='shoppingcart_r')


class Subscriber(Base):
    __tablename__ = 'subscriber'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    author_id = Column(Integer, ForeignKey('users.id'))
