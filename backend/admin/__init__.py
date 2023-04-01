import logging

from typing import cast

from flask import Flask
from flask_admin import Admin, AdminIndexView
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker

from .config import Config
from .views import *

import sys
sys.path.append('..')

from database import engine
from models import Tag, Ingredient, Recipe, User
from routers.auth import get_db

current_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine
))

def create_app() -> Flask:
    app = Flask(__name__, static_folder='static', static_url_path='/admin/static')
    app.config.from_object(Config)
    app.config['FLASK_ADMIN_SWATCH'] = 'Cosmo'
    app.secret_key = 'kek'


    # login_manager = LoginManager()
    # login_manager.init_app(app)

    # Create user loader function
    # @app.before_first_request
    # def restrict_admin_url():
    #     endpoint = 'admin.index'
    #     url = url_for(endpoint)
    #     admin_index = app.view_functions.pop(endpoint)

        # @app.route(url, endpoint=endpoint)
        # @roles_required('admin')
        # def secure_admin_index():
        #     return admin_index()

    admin = Admin(app, name='Foodgram', index_view=AdminIndexView(name='Foodgram index', url='/admin/'), template_mode='bootstrap4')

    admin.add_view(UserView(User, current_session))
    admin.add_view(TagView(Tag, current_session))
    admin.add_view(IngredientView(Ingredient, current_session))
    admin.add_view(RecipeView(Recipe, current_session))
    admin.add_sub_category(name="IngredientAmount", parent_name="Ingredient")

    return cast(Flask, admin.app)


app = create_app()

db = SQLAlchemy(app)
# app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('FastAPI diploma startup')

login_manager = LoginManager(app)
# login_manager.init_app(app)
login_manager.login_view = 'login'

# @login_manager.user_loader
# def login_loader(user_id):
#     return User.query.get(user_id)
#     # return db.query(User).get(user_id)

from admin import models


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': models.User}