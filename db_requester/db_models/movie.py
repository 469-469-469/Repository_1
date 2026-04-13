from sqlalchemy import Column, String, Boolean, DateTime, Float, Integer
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class MovieDBSheme(Base):
    __tablename__ = 'movies'

    id = Column(String, primary_key=True)
    name = Column(String)
    price = Column(Float)
    description = Column(String)
    image_url = Column(String)
    location = Column(String)
    published = Column(Boolean)
    genre_id = Column(Float)
    created_at = Column(DateTime)