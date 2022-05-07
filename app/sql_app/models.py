from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sql_app.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(32), unique=True, index=True)
    password = Column(String(128))
    name = Column(String(128))


class Banner(Base):
    __tablename__ = 'banner'
    id = Column(Integer, primary_key=True, index=True)
    image = Column(String(128), index=True)
    content = Column(String(256))
    id_song = Column(Integer)
