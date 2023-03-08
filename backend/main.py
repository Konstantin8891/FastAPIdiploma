from fastapi import FastAPI
from fastapi.routing import Mount
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination
from piccolo_admin.endpoints import create_admin
from piccolo.engine import engine_finder

# from admin.tables import PiccoloTag
from database import SessionLocal
from routers import users, tags, ingredients, recipes, auth


def configure_media(app): 
    # app.mount("/api/recipes/images", StaticFiles(directory="media"), name="media")
    app.mount("/media", StaticFiles(directory="media"), name="media")

def start_application():
    # app = FastAPI(routes=[Mount(path='/admin/', app=create_admin(
    #     tables=[PiccoloTag, ],
    #     site_name='Foodgram admin'
    # ))]) # Добавить таблицы, добавить allowed_hosts для https
    app = FastAPI()
    configure_media(app)
    return app

app = start_application()
# app = FastAPI()
app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(auth.router)
app.include_router(users.router)
add_pagination(app)
app.include_router(tags.router)
app.include_router(ingredients.router)
app.include_router(recipes.router)


# @app.on_event('startup')
# async def open_database_connection_pool():
#     engine = engine_finder()
#     await engine.start_connection_pool()


# @app.on_event('shutdown')
# async def close_database_connection_pool():
#     engine = engine_finder()
#     await engine.close_connection_pool()
