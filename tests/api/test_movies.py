from typing import Union

import pytest
from tests.api.api_manager import ApiManagerMovies, ApiManagerAuth
from faker import Faker
import logging

logger = logging.getLogger(__name__)
fake = Faker("ru_RU")
MISSING = object()


class TestMoviesAPIHappyPath:

    def test_create_movie(self, admin_api: ApiManagerAuth, test_movie: dict,
                          api_manager_movies: ApiManagerMovies):
        # Создание фильма
        logger.info("Позитивный тест. Создание фильма")

        data = test_movie
        response = api_manager_movies.movies_api.create_movie(data)
        response_created = response.json()
        assert "id" in response_created
        assert "name" in response_created
        assert "price" in response_created
        assert "description" in response_created

    def test_get_one_movie(self, api_manager_movies: ApiManagerMovies, movie: dict):
        # Получение фильма
        logger.info("Позитивный тест. Получение фильма")

        response = api_manager_movies.movies_api.get_movie(movie["id"])
        response_got = response.json()
        assert "id" in response_got
        assert "name" in response_got
        assert "price" in response_got
        assert "description" in response_got

    def test_change_movie(self, admin_api:ApiManagerAuth,api_manager_movies: ApiManagerMovies,movie: dict):
        # Редактирование фильма
        logger.info("Позитивный тест. Редактирование фильма")

        data = movie.copy()
        data["name"] = fake.sentence(nb_words=3)
        data["description"] = fake.sentence(nb_words=8)
        response = api_manager_movies.movies_api.change_movie(movie["id"], data)
        response_changed = response.json()

        assert "id" in response_changed
        assert "price" in response_changed
        assert response_changed["name"] == data["name"]
        assert response_changed["description"] == data["description"]

    def test_delete_movie(self,admin_api: ApiManagerAuth,api_manager_movies: ApiManagerMovies,movie: dict):
        # Удаление фильма
        logger.info("Позитивный тест. Удаление фильма")
        api_manager_movies.movies_api.delete_movie(movie["id"])
        api_manager_movies.movies_api.get_movie(movie["id"], 404)


    @pytest.mark.parametrize("field_get, value_get", [
        ("Default", True),  # Не отправляем ничего
        ("page", MISSING),  # Не отправляем page
        ("pageSize", 1),    # Граничное значение
        ("minPrice", 1),    # Граничное значение
        ("maxPrice", 2),    # Граничное значение
        ("genreId", 1)      # Граничное значение
    ])
    def test_get_poster(self, api_manager_movies: ApiManagerMovies, test_poster: dict, field_get: str,
                        value_get: Union[str, None, object]):
        # Получение афиши с фильмами
        logger.info(f"Позитивный тест. Получение афиши. Проверка поля {field_get}={value_get}")

        if field_get == "Default": # Передаем пустой словарь, тест значений по умолчанию,
            data = {}
        else:
            data = test_poster.copy()
            if value_get is MISSING: # Отправляем словарь без одного ключа, тест значения по умолчанию
                data.pop(field_get, None)
            else:
                data[field_get] = value_get

            if data.get("minPrice", 0) > data.get("maxPrice", 0):
                data["minPrice"] = data["maxPrice"] - 1

        response = api_manager_movies.movies_api.get_poster_movie(data)
        response_data = response.json()

        # Проверки
        assert "movies" in response_data
        assert "pageCount" in response_data
        assert "count" in response_data
        assert "page" in response_data
        assert "pageSize" in response_data

        api_manager_movies.auth_api.logout()

        if response_data["movies"]:
            assert "id" in response_data["movies"][0]
        else:
            logger.info("Список фильмов пуст на этой странице")


class TestMoviesAPINegative:

    @pytest.mark.parametrize("field_create_negative, value_create_negative", [
        ("not_access", True),
        ("name", ""),
        ("name", MISSING)
    ])
    def test_create_movie(self, admin_api: ApiManagerAuth, test_movie: dict, api_manager_movies: ApiManagerMovies,
                          field_create_negative: str, value_create_negative: Union[str, None, object]):
        # Создание фильма
        logger.info(f"Негативный тест. Создание фильма. Проверка поля {field_create_negative}={value_create_negative}")

        data = test_movie.copy()
        if value_create_negative is MISSING:
            data.pop(field_create_negative, None)
        else:
            data[field_create_negative] = value_create_negative

        expected_status = 400
        if field_create_negative == "not_access":
            api_manager_movies.auth_api.logout()
            expected_status = 401

        api_manager_movies.movies_api.create_movie(data, expected_status)


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
    def test_get_poster_negative(self, api_manager_movies: ApiManagerMovies, test_poster: dict, field_negative: "str",
                                 value_negative: Union[str, None, object]):
        # Получение афиши с фильмами
        logger.info(f"Негативный тест. Получение афиши с фильмами. Проверка поля {field_negative}={value_negative}")

        data = test_poster.copy()
        data[field_negative] = value_negative

        expected_status = 400
        api_manager_movies.movies_api.get_poster_movie(data, expected_status)