import uvicorn

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.routing import Mount
from fastapi.staticfiles import StaticFiles
from fastapi_keycloak import FastAPIKeycloak, OIDCUser
from fastapi_pagination import add_pagination
# from piccolo_admin.endpoints import create_admin
# from piccolo.engine import engine_finder

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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": exc.errors()},
    )

# idp = FastAPIKeycloak(
#     server_url="http://localhost:8085/", # frontend
#     client_id="test-client",
#     client_secret="GzgACcJzhzQ4j8kWhmhazt7WSdxDVUyE",
#     admin_client_secret="BIcczGsZ6I8W5zf0rZg5qSexlloQLPKB",
#     realm="Test",
#     callback_uri="http://localhost:8000/callback"
# )
# idp.add_swagger_config(app)
# app = FastAPI()
app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(auth.router)
app.include_router(users.router)
add_pagination(app)
app.include_router(tags.router)
app.include_router(ingredients.router)
app.include_router(recipes.router)

# @app.get("/callback")
# def callback(session_state: str, code: str):
#     return idp.exchange_authorization_code(session_state=session_state, code=code)  # This will return an access token
# @app.on_event('startup')
# async def open_database_connection_pool():
#     engine = engine_finder()
#     await engine.start_connection_pool()


# @app.on_event('shutdown')
# async def close_database_connection_pool():
#     engine = engine_finder()
#     await engine.close_connection_pool()

# if __name__ == '__main__':
#     uvicorn.run('main:app', host="127.0.0.1", port=8000)
