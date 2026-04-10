from pydantic import BaseModel
from venv import logger
import pytest_check as check


class RequestTestMovie(BaseModel):
    name: str
    imageUrl: str
    price: float
    description: str
    location: str
    published: bool
    genreId: int


def pydantic_movie_request(test_movie: dict):
    pydantic_movie = RequestTestMovie(**test_movie)
    log_json = pydantic_movie.model_dump_json()
    logger.info(f"Логируем Pydantic {log_json}")  # а также возможность удобного взаимодействия
    return pydantic_movie.model_dump()  # <- возвращаем словарь


class ResponseTestMovie(BaseModel):
    name: str
    imageUrl: str
    price: float
    description: str
    location: str
    published: bool
    genreId: int


# Проверки данных фильма из ответа от сервера, + при получении request_movie сравнивается с ним
def pydantic_movie_response(response_movie: dict, request_movie: dict=None):
    pydantic_movie = ResponseTestMovie(**response_movie)
    log_json = pydantic_movie.model_dump_json()
    logger.info(f"Логируем Pydantic {log_json}")  # а также возможность удобного взаимодействия

    pydantic_movie = pydantic_movie.model_dump()  # <- превращаем в словарь
    if request_movie:
        fields_to_check = ["name", "price", "description"]
        for field in fields_to_check:
            check.equal(
                pydantic_movie.get(field),
                request_movie.get(field),
                f"{field} не совпадает с отправленным"
            )

    return pydantic_movie