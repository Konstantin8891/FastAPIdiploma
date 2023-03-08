import logging

from typing import cast

from flask import Flask
from flask_admin import Admin, AdminIndexView
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker

from .view import UserView, TagView, IngredientView, RecipeView 
from .config import Config

import sys
sys.path.append('..')

from database import engine

from models import *

# app = Flask(__name__)

# app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# admin = Admin(app, name='foodgram', template_mode='bootstrap3')

# app.run()

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
    # @login_manager.user_loader
    # def load_user(user_id):
    #     return User.query.get(user_id)

    admin = Admin(app, name='Foodgram', index_view=AdminIndexView(name='📃', url='/admin/'), template_mode='bootstrap4')

    admin.add_view(UserView(User, current_session))
    admin.add_view(TagView(Tag, current_session))
    admin.add_view(IngredientView(Ingredient, current_session))
    admin.add_view(RecipeView(Recipe, current_session))
    admin.add_sub_category(name="IngredientAmount", parent_name="Ingredient")

    return cast(Flask, admin.app)

# from db import DBSettings

# DBSettings().setup_db()

app = create_app()

# app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('FastAPI diploma startup')
# db = SQLAlchemy(app)

# login_manager = LoginManager(app)
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# @login_manager.user_loader
# def load_user(user):
#     return User.query.get(int(user))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
