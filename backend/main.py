from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_pagination import add_pagination

from database import SessionLocal
from routers import users, tags, ingredients, recipes, auth


def configure_media(app): 
    app.mount("/media", StaticFiles(directory="media"), name="media")


def start_application():
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
