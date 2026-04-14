from typing import Optional

import allure
from pydantic import BaseModel
from venv import logger


class RequestTestMovie(BaseModel):
    name: str
    imageUrl: str
    price: float
    description: str
    location: str
    published: bool
    genreId: int


@allure.step("Обработка отправляемых данных")
def pydantic_movie_request(test_movie: dict) -> RequestTestMovie:
    pydantic_movie = RequestTestMovie(**test_movie)
    log_json = pydantic_movie.model_dump_json()
    logger.info(f"Логируем Pydantic {log_json}")
    return pydantic_movie


class ResponseTestMovie(BaseModel):
    id: Optional[int] = None
    name: str
    imageUrl: str
    price: float
    description: str
    location: str
    published: bool
    genreId: int


def pydantic_movie_response(response_movie: dict) -> ResponseTestMovie:
    pydantic_movie = ResponseTestMovie(**response_movie)
    log_json = pydantic_movie.model_dump_json()
    logger.info(f"Логируем Pydantic {log_json}")

    pydantic_movie = pydantic_movie

    return pydantic_movie