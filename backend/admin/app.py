import logging

from typing import cast

from fastapi import Depends
from flask import Flask, url_for, flash, request, abort, redirect, render_template
from flask_admin import Admin, AdminIndexView
from flask_admin.helpers import is_safe_url
from flask_login import LoginManager, login_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from werkzeug.urls import url_parse

from admin import app

from .views import UserView, TagView, IngredientView, RecipeView 
# from .config import Config
from .forms import LoginForm

import sys
sys.path.append('..')

from database import engine
from models import Tag, Ingredient, Recipe, User
from routers.auth import get_db
from backend.routers.services.hash import verify_hash
 
# app = Flask(__name__)

# app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

# admin = Admin(app, name='foodgram', template_mode='bootstrap3')

# app.run()

# current_session = scoped_session(sessionmaker(
#     autocommit=False, autoflush=False, bind=engine
# ))

# def create_app() -> Flask:
#     app = Flask(__name__, static_folder='static', static_url_path='/admin/static')
#     app.config.from_object(Config)
#     app.config['FLASK_ADMIN_SWATCH'] = 'Cosmo'
#     app.secret_key = 'kek'


#     # login_manager = LoginManager()
#     # login_manager.init_app(app)

#     # Create user loader function
#     # @app.before_first_request
#     # def restrict_admin_url():
#     #     endpoint = 'admin.index'
#     #     url = url_for(endpoint)
#     #     admin_index = app.view_functions.pop(endpoint)

#         # @app.route(url, endpoint=endpoint)
#         # @roles_required('admin')
#         # def secure_admin_index():
#         #     return admin_index()

#     admin = Admin(app, name='Foodgram', index_view=AdminIndexView(name='📃', url='/admin/'), template_mode='bootstrap4')

#     admin.add_view(UserView(User, current_session))
#     admin.add_view(TagView(Tag, current_session))
#     admin.add_view(IngredientView(Ingredient, current_session))
#     admin.add_view(RecipeView(Recipe, current_session))
#     admin.add_sub_category(name="IngredientAmount", parent_name="Ingredient")

#     return cast(Flask, admin.app)


# from db import DBSettings

# DBSettings().setup_db()

# app = create_app()

# db = SQLAlchemy(app)
# # app.logger.addHandler(file_handler)
# app.logger.setLevel(logging.INFO)
# app.logger.info('FastAPI diploma startup')

# login_manager = LoginManager(app)
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# @login_manager.user_loader
# def login_loader(user_id):
#     return User.query.get(user_id)

# @app.route('/admin/login', methods=['GET', 'POST'])
# def login():
#     # if current_user.is_authenticated:
#     #     return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         # user = db.query(User).filter_by(username=form.username.data).first()
#         user = User.query.filter_by(username=form.username.data).first()
#         print(user)
#         app.logger.info('user = ', user)
#         if user is None or not verify_password(form.password.data, user.password):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('admin.index')
#         return redirect(next_page)
#     return render_template('admin/login.html', title='Sign In', form=form)
# db = SQLAlchemy(app)

# login_manager = LoginManager(app)
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# @login_manager.user_loader
# def load_user(user):
#     return User.query.get(int(user))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
