import logging
import random
from typing import Any, Generator, Callable

from faker import Faker
from uuid import uuid4
import pytest
import requests
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from db_requester.db_helpers import DBHelper

from constants import REGISTER_ENDPOINT, BASE_URL_MOVIES, BASE_URL_AUTH, BASE_URL_PAYMENT
from constants.roles import Roles
from custom_requester.custom_requester import CustomRequester
from entities.user import User
from models.movies_base_models import pydantic_movie_request
from models.users_base_models import pydantic_user_request
from resources.user_creds import SuperAdminCreds
from utils.api.api_manager import ApiManager
from utils.data_generator import DataGenerator


faker = Faker()
fake_ru = Faker("ru_RU")

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
def user_session(session: Session):
    """Фабрика сессий пользователей."""
    user_pool = []

    def _create_user_session():
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


# ----------------------------
# Данные для тестов
# ----------------------------


@pytest.fixture
def test_user():
    """Генерация случайных параметров для создания пользователя."""
    random_password = DataGenerator.generate_random_password()

    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }


@pytest.fixture(scope="function")
def creation_user_data(test_user: dict):
    """Добавление полей пользователю."""
    updated_data = test_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return pydantic_user_request(updated_data)


@pytest.fixture
def registration_user_data():
    random_password = DataGenerator.generate_random_password()

    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }


@pytest.fixture()
def test_movie():
    """Генерация случайных параметров для создания фильма."""
    data_movie = {
        "name": f"{fake_ru.sentence(nb_words=3)}_{uuid4()}",
        "imageUrl": f"https://{fake_ru.domain_name()}/image/{fake_ru.uuid4()}",
        "price": random.randint(100, 400),
        "description": fake_ru.sentence(nb_words=10),
        "location": "SPB",
        "published": True,
        "genreId": random.randint(1, 4)
    }
    return pydantic_movie_request(data_movie)


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
def movie(test_movie: dict, super_admin: User):
    """Создание фильма для использования в тесте."""
    response = super_admin.api.movies_api.create_movie(test_movie)
    response_data = response.json()
    movie_created = test_movie.copy()
    movie_created["id"] = response_data["id"]

    yield movie_created
    # Удаляем тестовый фильм
    try:
        super_admin.api.movies_api.delete_movie(movie_created["id"], expected_status=(200, 404))
    except Exception as e:
        logging.warning(f"Не удалось удалить тестовый фильм: {e}")


# ----------------------------
# Аутентификация
# ----------------------------


@pytest.fixture(scope="session")
def super_admin(user_session: Callable[..., ApiManager]):
    """Логиним super_admin."""
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session
    )

    # Аутентификация супер-админа и сохранение токена
    token = super_admin.api.auth_api.authenticate(super_admin.creds)
    super_admin.token = token  # на всякий случай, хотя authenticate уже это делает

    # Устанавливаем токен в CustomRequester для всех API
    super_admin.api.movies_api.requester.set_auth_token(token)
    super_admin.api.user_api.requester.set_auth_token(token)
    super_admin.api.payment_api.requester.set_auth_token(token)

    return super_admin


@pytest.fixture
def logged_in_super_admin(super_admin: User):
    """Логиним super_admin и обновляем токены для всех requester."""
    response = super_admin.api.auth_api.login_user(super_admin.creds)
    token = response.json()['accessToken']

    super_admin.token = token
    super_admin.api.movies_api.requester.set_auth_token(token)
    super_admin.api.user_api.requester.set_auth_token(token)
    super_admin.api.payment_api.requester.set_auth_token(token)

    return super_admin


@pytest.fixture
def common_user(user_session: Callable[..., ApiManager], super_admin: User, creation_user_data: dict):
    """Логиним Обычного пользователя."""
    creation_user_data["email"] = DataGenerator.generate_random_email()
    creation_user_data["fullName"] = DataGenerator.generate_random_name()
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture(scope="session")
def authorized_user(super_admin: User, registered_user: dict):
    """Аутентификация зарегистрированного пользователя."""
    super_admin.api.auth_api.authenticate(
        registered_user["email"],
        registered_user["password"]
    )
    return registered_user


# ----------------------------
# Регистрация пользователя
# ----------------------------


@pytest.fixture()
def registered_user(creation_user_data: dict, super_admin: User):
    """Фикстура для регистрации и получения данных зарегистрированного пользователя."""

    response = super_admin.api.auth_api.register_user(creation_user_data)
    response_data = response.json()
    registered = creation_user_data.copy()
    registered["id"] = response_data["id"]

    yield registered
    # Удаляем тестового пользователя
    try:
        super_admin.api.user_api.delete_user(registered["id"], expected_status=(200, 404))
    except Exception as e:
        logging.warning(f"Не удалось удалить тестового пользователя: {e}")


# ----------------------------
# Работа с БД
# ----------------------------


@pytest.fixture(scope="module")
def db_session() -> Generator[Any, Any, None]:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()


@pytest.fixture(scope="function")
def db_helper(db_session: Session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper


@pytest.fixture(scope="function")
def db_created_test_user(db_helper: DBHelper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)