import logging
import os
from dotenv import load_dotenv
import random
from faker import Faker
import pytest
import requests
from requests import Session

from constants import REGISTER_ENDPOINT, BASE_URL_AUTH, BASE_URL_MOVIES, MOVIE_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from tests.api.api_manager import ApiManagerAuth, ApiManagerMovies, ApiManagerPayment
from utils.data_generator import DataGenerator


faker = Faker()

# Загружаем логин пароль Администратора из .env
load_dotenv()

# ----------------------------
# Сессия и HTTP-клиенты
# ----------------------------

@pytest.fixture(scope="session")
def session():
    """Фикстура для создания HTTP-сессии."""
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def requester(session:Session):
    """Фикстура для создания экземпляра CustomRequester."""
    return CustomRequester(session)


@pytest.fixture(scope="session")
def api_manager_auth(session:Session):
    """Фикстура для создания экземпляра ApiManagerAuth."""
    return ApiManagerAuth(session)


@pytest.fixture(scope="session")
def api_manager_movies(session:Session):
    """Фикстура для создания экземпляра ApiManagerMovies."""
    return ApiManagerMovies(session)


@pytest.fixture(scope="session")
def api_manager_payment(session:Session):
    """Фикстура для создания экземпляра ApiManagerPayment."""
    return ApiManagerPayment(session)


# ----------------------------
# Данные для тестов
# ----------------------------

@pytest.fixture()
def test_user():
    """Генерация случайного пользователя для тестов."""
    random_password = DataGenerator.generate_random_password()
    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }


@pytest.fixture()
def test_movie():
    """Генерация случайных параметров для создания фильма."""
    fake_local = Faker("ru_RU")
    return {
        "name": fake_local.sentence(nb_words=3),
        "imageUrl": f"https://{fake_local.domain_name()}/image/{fake_local.uuid4()}",
        "price": random.randint(100, 400),
        "description": fake_local.sentence(nb_words=10),
        "location": "SPB",
        "published": True,
        "genreId": random.randint(1, 4)
    }


@pytest.fixture()
def test_poster():
    """Генерация случайных параметров для просмотра афиши."""
    max_price = random.randint(400, 500)
    return {
        "pageSize": random.randint(1, 20),
        "page": random.randint(1, 5),
        "minPrice": random.randint(1, max_price - 1),
        "maxPrice": max_price,
        "locations": "MSK",
        "published": True,
        "genreId": random.randint(1, 5)
    }


@pytest.fixture()
def movie(admin_api: ApiManagerAuth, requester: CustomRequester, test_movie: dict):
    """Создание фильма для использования в тесте."""
    response = requester.send_request(
        method="POST",
        base_url=BASE_URL_MOVIES,
        endpoint=MOVIE_ENDPOINT,
        data=test_movie,
        expected_status=201 # Падение теста, если пользователь не создан
    )
    response_data = response.json()
    movie_created = test_movie.copy()
    movie_created["id"] = response_data["id"]

    yield movie_created
    if movie_created.get("id"):  # Удаляем тестовый фильм
        delete_resource(requester, del_res=movie_created, url_for_delete=BASE_URL_MOVIES, endpoint_for_delete="/movies")


def delete_resource(requester: CustomRequester, del_res: dict, url_for_delete: str,
                    endpoint_for_delete: str):
    try:  # Удаление тестового ресурса после отработки теста, но тест не падает, если не удастся удалить
        requester.send_request(
            method="DELETE",
            base_url=url_for_delete,
            endpoint=f"{endpoint_for_delete}/{del_res['id']}",
            expected_status=200
        )
    except Exception as e:
        logging.warning(f"Не удалось удалить тестовый ресурс: {e}")


# ----------------------------
# Аутентификация
# ----------------------------

@pytest.fixture()
def admin_api(api_manager_auth: ApiManagerAuth):
    """Аутентификация под админом для тестов с правами администратора."""
    api_manager_auth.auth_api.authenticate(os.getenv("SUPER_ADMIN_EMAIL"),
    os.getenv("SUPER_ADMIN_PASSWORD"))
    return api_manager_auth


@pytest.fixture()
def authorized_user(api_manager_auth: ApiManagerAuth, registered_user: dict):
    """Аутентификация зарегистрированного пользователя."""
    api_manager_auth.auth_api.authenticate(
        registered_user["email"],
        registered_user["password"]
    )
    return registered_user


@pytest.fixture(autouse=True)
def logout_before_test(api_manager_auth: ApiManagerAuth):
    """Автоматический logout перед каждым тестом, только если пользователь залогинен."""
    auth_headers = api_manager_auth.auth_api.headers
    session_headers = getattr(api_manager_auth.session, "headers", {})

    if "authorization" in auth_headers or "authorization" in session_headers:
        api_manager_auth.auth_api.logout()

# ----------------------------
# Регистрация пользователя
# ----------------------------

@pytest.fixture()
def registered_user(requester: CustomRequester, test_user: dict):
    """Фикстура для регистрации и получения данных зарегистрированного пользователя."""
    response = requester.send_request(
        method="POST",
        base_url=BASE_URL_AUTH,
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201 # Падение теста если пользователь не создан
    )
    response_data = response.json()
    registered = test_user.copy()
    registered["id"] = response_data["id"]

    yield registered
    if registered.get("id"):  # Удаляем тестового пользователя
        delete_resource(requester, del_res=registered, url_for_delete=BASE_URL_MOVIES, endpoint_for_delete="/user")
