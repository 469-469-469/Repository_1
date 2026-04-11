from typing import Union, Iterable

import allure
import pytest

from db_requester.db_helpers import DBHelper
from entities.user import User
from faker import Faker
import logging

from models.movies_base_models import pydantic_movie_response

logger = logging.getLogger(__name__)
fake = Faker("ru_RU")
MISSING = object()

@allure.epic("Cinescop")
@allure.feature("movies_api")
@allure.tag("positive")
class TestMoviesAPIHappyPath:

    @allure.title("Позитивный тест. Создание фильма")
    @allure.tag("critical", "movies")
    @pytest.mark.api
    @pytest.mark.movies
    @pytest.mark.positive
    @pytest.mark.critical
    def test_create_movie(self, super_admin: User, test_movie: dict):
        logger.info("Позитивный тест. Создание фильма")

        data = test_movie
        response = super_admin.api.movies_api.create_movie(data)
        response_created = response.json()

        with allure.step("Проверка ответа от сервера на соответствие модели"):# request_movie - не обязательный параметр
            pydantic_movie_response(response_movie=response_created, request_movie=test_movie)


    @allure.title("Позитивный тест. Получение фильма")
    @allure.tag("critical", "movies")
    @pytest.mark.api
    @pytest.mark.movies
    @pytest.mark.positive
    @pytest.mark.critical
    def test_get_one_movie(self, super_admin: User, movie: dict):
        logger.info("Позитивный тест. Получение фильма")

        response = super_admin.api.movies_api.get_movie(movie["id"])
        response_got = response.json()

        with allure.step("Проверка ответа от сервера на соответствие модели"):# request_movie - не обязательный параметр
            pydantic_movie_response(response_movie=response_got)


    @allure.title("Позитивный тест. Редактирование фильма с проверкой изменений в БД")
    @allure.tag("critical", "movies")
    @pytest.mark.api
    @pytest.mark.movies
    @pytest.mark.positive
    @pytest.mark.critical
    def test_change_movie(self, super_admin: User, movie: dict, db_helper: DBHelper):
        logger.info("Позитивный тест. Редактирование фильма с проверкой изменений в БД")

        data = movie.copy()
        data["name"] = fake.sentence(nb_words=3)
        data["description"] = fake.sentence(nb_words=8)
        response = super_admin.api.movies_api.change_movie(movie["id"], data)
        response_changed = response.json()

        with allure.step("Проверка ответа от сервера на соответствие модели"):# request_movie - не обязательный параметр
            pydantic_movie_response(response_movie=response_changed, request_movie=data)

        with allure.step("Проверка на соответствие из базы данных"):
            db_movie = db_helper.get_movie_by_id(movie["id"])
            assert db_movie.name == data["name"], "Название фильма не изменилось в базе данных"
            assert db_movie.description == data["description"], "Описание фильма не изменилось в базе данных"


    @allure.title("Позитивный тест. Удаление фильма")
    @allure.tag("critical", "movies")
    @pytest.mark.api
    @pytest.mark.movies
    @pytest.mark.positive
    @pytest.mark.critical
    def test_delete_movie(self, super_admin: User, movie: dict):
        logger.info("Позитивный тест. Удаление фильма")
        super_admin.api.movies_api.delete_movie(movie["id"])
        super_admin.api.movies_api.get_movie(movie["id"], (404,))


    @allure.title("Позитивный тест. Получение афиши")
    @allure.tag("regression", "movies")
    @pytest.mark.api
    @pytest.mark.movies
    @pytest.mark.positive
    @pytest.mark.regression
    @pytest.mark.parametrize("field_get, value_get", [
        ("Default", True),  # Не отправляем ничего
        ("page", MISSING),  # Не отправляем page
        ("pageSize", 1),    # Граничное значение
        ("minPrice", 1),    # Граничное значение
        ("maxPrice", 2),    # Граничное значение
        ("genreId", 1)      # Граничное значение
    ])
    def test_get_poster(self, super_admin: User, test_poster: dict, field_get: str,
                        value_get: Union[str, None, object]):
        logger.info(f"Позитивный тест. Получение афиши. Проверка поля {field_get}={value_get}")

        if field_get == "Default": # Передаем пустой словарь, тест значений по умолчанию,
            data = {}
        else:
            data = test_poster.copy()
            if value_get is MISSING: # Отправляем словарь без одного ключа, тест значения по умолчанию
                data.pop(field_get, None)
            else:
                data[field_get] = value_get

            if data.get("maxPrice", 0) <= data.get("minPrice", 0):
                data["maxPrice"] = data["minPrice"] + 1

        response = super_admin.api.movies_api.get_poster_movie(data)
        response_data = response.json()


        # Проверки
        assert "movies" in response_data
        assert "pageCount" in response_data
        assert "count" in response_data
        assert "page" in response_data
        assert "pageSize" in response_data

        super_admin.api.auth_api.logout()

        if response_data["movies"]:
            assert "id" in response_data["movies"][0]
        else:
            logger.info("Список фильмов пуст на этой странице")


@allure.epic("Cinescop")
@allure.feature("movies_api")
@allure.tag("negative")
class TestMoviesAPINegative:

    @allure.title("Негативный тест. Создание фильма")
    @allure.tag("movies")
    @pytest.mark.api
    @pytest.mark.movies
    @pytest.mark.negative
    @pytest.mark.parametrize("field_create_negative, value_create_negative, expected_status_cr_neg", [
        pytest.param("not_access",True,(401,),marks=[pytest.mark.rbac,pytest.mark.critical]), # тест без доступа
        pytest.param("name", "", (400,), marks=pytest.mark.regression),  # пустое поле name
        pytest.param("name", MISSING, (400,), marks=pytest.mark.regression)  # отсутствующее поле name
    ])
    def test_create_movie(
            self,
            logged_in_super_admin: User,
            test_movie: dict,
            field_create_negative: str,
            value_create_negative: Union[str, None, object],
            expected_status_cr_neg: Iterable[int]
    ):
        logger.info(f"Негативный тест. Создание фильма. Проверка поля {field_create_negative}={value_create_negative}")

        data = test_movie.copy()

        # Случай отсутствия доступа
        if field_create_negative == "not_access":
            logged_in_super_admin.api.auth_api.logout()
            logged_in_super_admin.clear_tokens()
        else:
            # Подготавливаем данные для проверки поля
            if value_create_negative is MISSING:
                data.pop(field_create_negative, None)
            else:
                data[field_create_negative] = value_create_negative

        logged_in_super_admin.api.movies_api.create_movie(data, expected_status_cr_neg)


    @allure.title("Негативный тест. Получение афиши с фильмами")
    @allure.tag("regression", "movies")
    @pytest.mark.api
    @pytest.mark.movies
    @pytest.mark.negative
    @pytest.mark.regression
    @pytest.mark.parametrize("field_negative, value_negative", [
        ("page", 0),        # Невалидные граничные значения
        ("page", 0),        # Невалидные граничные значения
        ("pageSize", 0),    # Невалидные граничные значения
        ("pageSize", 21),   # Невалидные граничные значения
        ("minPrice", 0),    # Невалидные граничные значения
        ("maxPrice", 1),    # Невалидные граничные значения
        ("minPrice", 10000),# minPrice > maxPrice
        ("page", "abc"),    # Невалидные значения
        ("pageSize", "abc"),# Невалидные значения
        ("minPrice", "abc"),# Невалидные значения
        ("maxPrice", "abc"),# Невалидные значения
        ("genreId", "abc")  # Невалидные значения
    ])
    def test_get_poster_negative(self, super_admin: User, test_poster: dict, field_negative: str,
                                 value_negative: Union[str, None, object]):
        logger.info(f"Негативный тест. Получение афиши с фильмами. Проверка поля {field_negative}={value_negative}")

        data = test_poster.copy()
        data[field_negative] = value_negative

        expected_status = (400,)
        super_admin.api.movies_api.get_poster_movie(data, expected_status)