import allure
from pydantic import BaseModel
from venv import logger


class RequestTestPoster(BaseModel):
    pageSize: int
    page: int
    minPrice: float
    maxPrice: float
    locations: str
    published: bool
    genreId: int


@allure.step("Обработка отправляемых данных")
def pydantic_poster_request(test_poster: dict) -> RequestTestPoster:
    pydantic_poster = RequestTestPoster(**test_poster)
    log_json = pydantic_poster.model_dump_json()
    logger.info(f"Логируем Pydantic {log_json}")
    return pydantic_poster