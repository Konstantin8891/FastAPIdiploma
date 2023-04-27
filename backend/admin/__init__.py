import logging

from typing import cast

from flask import Flask
from flask_admin import Admin, AdminIndexView
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.urls import url_parse

from .config import Config
from .views import *

import sys
sys.path.append('..')

from routers.services.hash import verify_hash
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

    admin = Admin(app, name='Foodgram index', index_view=AdminIndexView(url='/'), template_mode='bootstrap4')

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
# from . import routes

# @login_manager.user_loader
# def login_loader(user_id):
#     return User.query.get(user_id)
#     # return db.query(User).get(user_id)

from admin import models, routes, forms


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': models.User}


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         app.logger.info('user = ', user)
#         if user is None or not verify_password(form.password.data, user.password):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('index')
#         return redirect(next_page)
#     return render_template('admin/login.html', title='Sign In', form=form)