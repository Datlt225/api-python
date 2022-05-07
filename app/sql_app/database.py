import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# lấy thông tin tài khoản mysql
username = os.getenv('user')
password = os.getenv('password')
host = os.getenv('host')
database = os.getenv('database')
print(host, username, password, database)

SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://{username}:{password}@{host}/{database}?charset=utf8'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
