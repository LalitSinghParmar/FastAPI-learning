from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
from fastapi import HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from .config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:%s@{settings.DATABASE_HOSTNAME}/{settings.DATABASE_NAME}"%quote(settings.DATABASE_PASSWORD)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user = 'postgres', password='p@55w0rd',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         break

#     except Exception as e:
#         print('Error %s while connecting to DB',(str(e)))
#         time.sleep(2)