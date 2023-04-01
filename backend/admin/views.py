from fastapi import Depends
from flask import url_for, request, redirect, flash, abort, redirect, render_template
from flask_login import current_user, login_user
from flask_admin import form
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin.helpers import is_safe_url
from markupsafe import Markup
from sqlalchemy.orm import selectinload, joinedload, scoped_session, sessionmaker, Session
from wtforms import StringField, TextAreaField, validators

from .forms import LoginForm

import sys
sys.path.append('..')

from database import SessionLocal, engine
from models import Favorite, IngredientAmount, Image, User
from routers.recipes import get_db

PAGE_SIZE = 10


class UserView(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True
    page_size = PAGE_SIZE

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))
    
    


class TagView(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True
    page_size = PAGE_SIZE

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class IngredientView(ModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True
    page_size = PAGE_SIZE

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class RecipeView(ModelView):
    can_edit = True
    can_create = False
    can_delete = True
    can_view_details = True
    column_display_pk = True
    column_display_all_relations = True
    column_filters = ('name', 'author.username', 'tags.name')
    column_exclude_list = ('favorites_r', 'shoppingcart_r')
    column_details_exclude_list = ('favorites_r', 'shoppingcart_r')
    # create_template = 'create_recipe.html'
    inline_models = ((
        IngredientAmount,
        {
            'form_columns': ('id', 'amount', 'ingredient'),
        }
    ),) 
    page_size = 10 
    column_list = (
        'id',
        'name',
        'text',
        'cooking_time',
        'image',
        'ingredients',
        'tags',
        'author',
        'created',
        'favorites'
    )

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))
