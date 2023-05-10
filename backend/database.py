from redis import Redis, ConnectionPool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/FastAPIdiploma_db"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@postgres_db:5432/postgres"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

pool = ConnectionPool(host='localhost', port=6379, db=0)
redis_db = Redis(connection_pool=pool, password='redis')
