from fastapi import Depends
from flask import url_for, request, redirect, flash, abort, redirect, render_template
from flask_login import current_user, login_user
from flask_admin import form
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.view import log
from flask_admin.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin.helpers import is_safe_url
from markupsafe import Markup
from sqlalchemy.orm import selectinload, joinedload, scoped_session, sessionmaker, Session
from wtforms import StringField, TextAreaField, validators, IntegerField

from .forms import LoginForm

import sys
sys.path.append('..')

from database import SessionLocal, engine
from models import Favorite, IngredientAmount, Image, User
from routers.recipes import get_db
from routers.services.hash import get_hash

PAGE_SIZE = 10


class AddAuthorizationModelView(ModelView):
    list_template = 'admin/list.html'
    edit_template = 'admin/edit.html'
    create_template = 'admin/create.html'
    details_template = 'admin/details.html'

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))


class UserView(AddAuthorizationModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True
    page_size = PAGE_SIZE

    def create_model(self, form):
        """
            Create model from form.

            :param form:
                Form instance
        """
        try:
            model = self.build_new_instance()
            print(form.password.data)
            form.password.data = get_hash(form.password.data)
            form.populate_obj(model)
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to create record. %(error)s', error=str(ex)), 'error')
                log.exception('Failed to create record.')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, True)

        return model


class TagView(AddAuthorizationModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True
    page_size = PAGE_SIZE
    form_widget_args = {
        'recipes':{
            'disabled': True
        }
    }


class IngredientView(AddAuthorizationModelView):
    can_edit = True
    can_create = True
    can_delete = True
    can_view_details = True
    page_size = PAGE_SIZE
    column_list = ('id', 'name', 'measurement_unit', )
    form_widget_args = {
        'ingredient_amount':{
            'disabled': True
        }
    }


class RecipeView(AddAuthorizationModelView):
    can_edit = True
    can_create = False
    can_delete = True
    can_view_details = True
    column_display_pk = True
    column_display_all_relations = True
    column_filters = ('name', 'author.username', 'tags.name')
    column_exclude_list = ('favorites_r', 'shoppingcart_r')
    column_details_exclude_list = ('favorites_r', 'shoppingcart_r')
    list_template = 'admin/list.html'
    edit_template = 'admin/edit.html'
    create_template = 'admin/create.html'
    details_template = 'admin/details.html'
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
