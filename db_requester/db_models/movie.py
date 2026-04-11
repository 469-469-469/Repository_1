from sqlalchemy import Column, String, Boolean, DateTime, Float
from sqlalchemy.orm import declarative_base
from typing import Dict, Any

Base = declarative_base()


class MovieDBModel(Base):
    __tablename__ = 'movies'

    id = Column(String, primary_key=True)  # text в БД
    name = Column(String)  # text в БД
    price = Column(Float)  # число в БД
    description = Column(String)  # text в БД
    image_url = Column(String)  # timestamp в БД
    location = Column(String)  # bool в БД
    published = Column(Boolean)  # bool в БД
    genre_id = Column(Float)  # число в БД
    created_at = Column(DateTime)  # timestamp в БД