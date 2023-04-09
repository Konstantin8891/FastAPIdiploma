from datetime import datetime, timedelta
from fastapi.security import OAuth2AuthorizationCodeBearer, SecurityScopes


from fastapi import APIRouter, Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from .services.authenticate import authenticate_user
from .services.hash import get_hash, verify_hash

import sys
sys.path.append('..')

import models

from database import SessionLocal, redis_db
from schemas import CreateToken


SECRET_KEY = "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"

oauth2_bearer = OAuth2AuthorizationCodeBearer(authorizationUrl="token", tokenUrl="token")
oauth2_bearer_optional = OAuth2AuthorizationCodeBearer(authorizationUrl="token", tokenUrl="token", auto_error=False)

router = APIRouter(prefix='/api/auth', tags=['auth'])


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_user_and_hashed_token(db: Session, user: dict):
    # print(user)
    user_instance = db.query(models.User).get(user.get('id'))
    token_hashed = redis_db.get(user_instance.username)
    if token_hashed:
        token_hashed = token_hashed.decode('utf-8')
    return user_instance, token_hashed


async def get_user_or_none(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_bearer_optional)
):
    if token is None:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("id")
        if email is None or user_id is None:
            raise HTTPException(status_code=401, detail='User not found')
        return {"email": email, "id": user_id, "token": token}
    except JWTError:
        raise HTTPException(status_code=404, detail='User not found')


async def get_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_bearer)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("id")
        if email is None or user_id is None:
            raise HTTPException(status_code=401, detail='User not found')
        return {"email": email, "id": user_id, "token": token}
    except JWTError:
        raise HTTPException(status_code=404, detail='User not found')


# async def get_user_and_expire_token(
#     security_scopes: SecurityScopes, token: str = Depends(oauth2_bearer)
# ):
#     try:
#         # token.payload['exp'] = datetime.utcnow()
#         print(token)
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         print(payload)
#         email: str = payload.get("sub")
#         user_id: int = payload.get("id")
#         if email is None or user_id is None:
#             raise HTTPException(status_code=401, detail='User not found')
#         return {"email": email, "id": user_id}
#     except JWTError:
#         raise HTTPException(status_code=404, detail='User not found')


@router.post('/token/login/')
async def get_token(credentials: CreateToken, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if user is None:
        raise HTTPException(status_code=400, detail='User not found')
    authenticate_user(user.username, credentials.password, db)
    encode = {"sub": credentials.email, "id": user.id, "expired": False}
    expire = datetime.utcnow() + timedelta(minutes=60)
    encode.update({"exp": expire})
    expire = timedelta(minutes=60).total_seconds() * 1000
    expire = int(expire)
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    token_hash = get_hash(token)
    redis_db.set(user.username, token_hash)
    redis_db.setex(user.username, str(expire), token_hash)
    return {"auth_token": token}


@router.post('/token/logout/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_token(user: dict = Security(get_user), db: Session = Depends(get_db)):
    user_instance, token_hashed = get_user_and_hashed_token(db, user)
    if token_hashed is None:
        raise HTTPException(status_code=401, detail='Unauthorized')
    if token_hashed and verify_hash(user.get('token'), token_hashed):
        redis_db.delete(user_instance.username)

    # encode = {"sub": user_.email, "id": user.id}
    # expire = datetime.utcnow()
    # encode.update({"exp": expire})
    # token = jwt.encode(encode, SECRET_KEY)
    # print(token)
    # jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    return 'deleted'

# from fastapi import Response
# from fastapi_jwt_auth import AuthJWT
# from pydantic import EmailStr, BaseModel
# from routers.services.password import verify_password
# import base64


# ACCESS_TOKEN_EXPIRES_IN = 30
# REFRESH_TOKEN_EXPIRES_IN = 60

# JWT_PRIVATE_KEY='LS0tLS1CRUdJTiBSU0EgUFJJVkFURSBLRVktLS0tLQpNSUlCT2dJQkFBSkJBSSs3QnZUS0FWdHVQYzEzbEFkVk94TlVmcWxzMm1SVmlQWlJyVFpjd3l4RVhVRGpNaFZuCi9KVHRsd3h2a281T0pBQ1k3dVE0T09wODdiM3NOU3ZNd2xNQ0F3RUFBUUpBYm5LaENOQ0dOSFZGaHJPQ0RCU0IKdmZ2ckRWUzVpZXAwd2h2SGlBUEdjeWV6bjd0U2RweUZ0NEU0QTNXT3VQOXhqenNjTFZyb1pzRmVMUWlqT1JhUwp3UUloQU84MWl2b21iVGhjRkltTFZPbU16Vk52TGxWTW02WE5iS3B4bGh4TlpUTmhBaUVBbWRISlpGM3haWFE0Cm15QnNCeEhLQ3JqOTF6bVFxU0E4bHUvT1ZNTDNSak1DSVFEbDJxOUdtN0lMbS85b0EyaCtXdnZabGxZUlJPR3oKT21lV2lEclR5MUxaUVFJZ2ZGYUlaUWxMU0tkWjJvdXF4MHdwOWVEejBEWklLVzVWaSt6czdMZHRDdUVDSUVGYwo3d21VZ3pPblpzbnU1clBsTDJjZldLTGhFbWwrUVFzOCtkMFBGdXlnCi0tLS0tRU5EIFJTQSBQUklWQVRFIEtFWS0tLS0t'
# JWT_PUBLIC_KEY='LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUZ3d0RRWUpLb1pJaHZjTkFRRUJCUUFEU3dBd1NBSkJBSSs3QnZUS0FWdHVQYzEzbEFkVk94TlVmcWxzMm1SVgppUFpSclRaY3d5eEVYVURqTWhWbi9KVHRsd3h2a281T0pBQ1k3dVE0T09wODdiM3NOU3ZNd2xNQ0F3RUFBUT09Ci0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLQ=='

# class Settings(BaseModel):
#     authjwt_algorithm = 'RS256'
#     authjwt_decode_algorithms = ['RS256', ]
#     authjwt_token_location = {'cookies', 'headers'}
#     authjwt_access_cookie_key = 'access_token'
#     authjwt_refresh_cookie_key = 'refresh_token'
#     authjwt_cookie_csrf_protect = False
#     authjwt_public_key: str = base64.b64decode(JWT_PUBLIC_KEY).decode('utf-8')
#     authjwt_private_key: str = base64.b64decode(JWT_PRIVATE_KEY).decode('utf-8')
#     # authjwt_secret_key = JWT_PUBLIC_KEY


# @AuthJWT.load_config
# def get_config():
#     return Settings()


# def require_user(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
#     try:
#         Authorize.jwt_required()
#         email = Authorize.get_jwt_subject()
#         user = db.query(models.User).filter(models.User.email == email).first()

#         if not user:
#             raise Exception('User no longer exist')

#     except Exception as e:
#         raise Exception('Email/pass error')
#     return email


# @router.post('/token/login/')
# def login(payload: CreateToken, response: Response, db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
#     # Check if the user exist
#     user = db.query(models.User).filter(
#         models.User.email == payload.email).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail='Incorrect Email or Password')

#     # Check if user verified his email
#     # if not user.verified:
#     #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#     #                         detail='Please verify your email address')

#     # Check if the password is valid
#     if not verify_password(payload.password, user.password):
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail='Incorrect Email or Password')

#     # Create access token
#     access_token = Authorize.create_access_token(
#         subject=str(user.email), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

#     # Create refresh token
#     refresh_token = Authorize.create_refresh_token(
#         subject=str(user.email), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

#     # Store refresh and access tokens in cookie
#     response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
#                         ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
#     response.set_cookie('refresh_token', refresh_token,
#                         REFRESH_TOKEN_EXPIRES_IN * 60, REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
#     response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
#                         ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')

#     # Send both access
#     return {'status': 'success', 'access_token': access_token}


# @router.post('/token/logout/', status_code=status.HTTP_204_NO_CONTENT)
# async def delete_token(user: dict = Security(get_user_and_expire_token), db: Session = Depends(get_db)):
#     user = db.query(models.User).get(user.get('id'))
#     encode = {"sub": user.email, "id": user.id}
#     expire = datetime.utcnow()
#     encode.update({"exp": expire})
#     token = jwt.encode(encode, SECRET_KEY)
#     print(token)
#     # jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
#     return 'deleted'


# @router.get('/token/logout/', status_code=status.HTTP_200_OK)
# def logout(response: Response, Authorize: AuthJWT = Depends(), email: str = Depends(require_user)):
#     Authorize.unset_jwt_cookies()
#     response.set_cookie('logged_in', '', -1)

#     return {'status': 'success'}
