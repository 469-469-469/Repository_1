import logging
import allure
import pytest
from db_requester.db_helpers import DBHelper
from entities.user import User
from models.users_base_models import pydantic_user_response, RequestTestUser, ResponseTestUser
from utils.assertions import assert_equal, assert_in

logger = logging.getLogger(__name__)


@allure.epic("Cinescop")
@allure.feature("auth_api")
@allure.tag("positive")
class TestAuthAPIHappyPath:

    @allure.title("Позитивный тест. Создание пользователя")
    @allure.tag("critical", "user")
    @pytest.mark.api
    @pytest.mark.user
    @pytest.mark.positive
    @pytest.mark.critical
    def test_create_user(self, super_admin: User, creation_user_data: RequestTestUser, db_helper: DBHelper):
        logger.info("Позитивный тест. Создание пользователя")

        response = super_admin.api.user_api.create_user(creation_user_data).json()
        with allure.step("Проверка ответа от сервера на соответствие модели"):
            pydantic_user_response(response_user=response)

        with allure.step("Проверка на соответствие из базы данных"):
            db_user = db_helper.get_user_by_id(response['id'])
            assert_equal(
                db_user.email,
                response['email'],
                name="Проверка соответствия email в базе данных"
            )

    @allure.title("Позитивный тест. Получение информации о пользователе по id и email")
    @allure.tag("critical", "user")
    @pytest.mark.api
    @pytest.mark.user
    @pytest.mark.positive
    @pytest.mark.critical
    def test_get_user_by_locator(self, super_admin: User, registered_user: ResponseTestUser):
        logger.info("Позитивный тест. Получение информации о пользователе по id и email")

        response_by_id = super_admin.api.user_api.get_user(registered_user.id).json()
        response_by_email = super_admin.api.user_api.get_user(registered_user.email).json()

        with allure.step("Проверка ответа от сервера на соответствие модели"):
            pydantic_user_response(response_user=response_by_id)
            pydantic_user_response(response_user=response_by_email)

        assert_equal(
            response_by_id,
            response_by_email,
            name="Содержание ответов должно быть идентичным"
        )


    @allure.title("Позитивный тест. Регистрация и авторизация пользователя")
    @allure.tag("smoke", "user")
    @pytest.mark.api
    @pytest.mark.user
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_register_and_login_user(self, super_admin: User, registered_user: ResponseTestUser):
        logger.info("Позитивный тест на регистрацию и авторизацию пользователя")
        login_data = {
            "email": registered_user.email,
            "password": registered_user.password
        }

        response = super_admin.api.auth_api.login_user(login_data)
        response_data = response.json()

        # Проверки
        assert_in("accessToken", response_data, "Проверка присутствия токена доступа в ответе")
        assert_equal(
            response_data["user"]["email"],
            registered_user.email,
            name="Сравнение Email в HTTP запросе и ответе от сервера"
        )


    @allure.title("Позитивный тест. Изменение пользователя с проверкой изменений в БД")
    @allure.tag("critical", "user")
    @pytest.mark.api
    @pytest.mark.user
    @pytest.mark.positive
    @pytest.mark.critical
    def test_change_user(self, super_admin: User, registered_user: ResponseTestUser, db_helper: DBHelper):
        logger.info("Позитивный тест. Изменение пользователя с проверкой изменений в БД")
        user_id = registered_user.id
        new_verified = True
        new_banned = False
        new_data = {"verified": new_verified, "banned": new_banned}
        response = super_admin.api.user_api.change_user(user_id, new_data, expected_status=(200,))
        response_data = response.json()

        with allure.step("Проверка ответа от сервера на соответствие модели"):
            pydantic_user_response(response_user=response_data)

        with allure.step("Проверка на соответствие из базы данных"):
            db_user = db_helper.get_user_by_id(registered_user.id)

            assert_equal(
                db_user.verified,
                new_verified,
                name="Проверка соответствия статуса verified в базе данных"
            )
            assert_equal(
                db_user.banned,
                new_banned,
                name="Проверка соответствия статуса banned в базе данных"
            )

        assert_equal(
            response_data["verified"],
            new_verified,
            name="Проверка, изменился ли статус верификации"
        )
        assert_equal(
            response_data["banned"],
            new_banned,
            name="Проверка, изменился ли статус banned"
        )


@allure.epic("Cinescop")
@allure.feature("auth_api")
@allure.tag("negative")
class TestAuthNegative:

    @allure.title("Негативный тест. Регистрация пользователя")
    @allure.tag("regression", "user")
    @pytest.mark.api
    @pytest.mark.user
    @pytest.mark.negative
    @pytest.mark.regression
    @pytest.mark.parametrize("field_register, value_register", [
        ("email", "abc"),         # некорректный email
        ("fullName", "")         # пустая строка
    ])
    def test_negative_register(self, super_admin: User, creation_user_data: RequestTestUser, field_register: str,
                               value_register: str):
        logger.info(f"Негативный тест. Регистрация пользователя. Проверка поля {field_register}={value_register}")

        data = creation_user_data.model_copy(update={field_register: value_register})

        expected_status = (400,)
        super_admin.api.auth_api.register_user(data.model_dump(), expected_status)


    @allure.title("Негативный тест. Авторизация пользователя")
    @allure.tag("user", "critical", "rbac")
    @pytest.mark.api
    @pytest.mark.user
    @pytest.mark.negative
    @pytest.mark.critical
    @pytest.mark.rbac
    @pytest.mark.parametrize("field_auth, value_auth", [
        pytest.param("email", "abc", marks=[pytest.mark.regression]),               # некорректный email
        pytest.param("email", "", marks=[pytest.mark.regression]),                  # пустая строка
        pytest.param("password", "", marks=[pytest.mark.rbac,pytest.mark.smoke]),   # пустая строка
        pytest.param("password", "1", marks=[pytest.mark.rbac,pytest.mark.smoke]),  # неверный пароль
    ])
    def test_negative_auth(self, super_admin: User, registered_user: ResponseTestUser, field_auth: str,
                           value_auth: str):
        logger.info(f"Негативный тест. Авторизация пользователя. Проверка поля {field_auth}={value_auth}")

        login_data = {"email": registered_user.email, "password": registered_user.password,
                      field_auth: value_auth}

        super_admin.api.auth_api.login_user(login_data)


    @allure.title("Негативный тест. Регистрация пользователя")
    @allure.tag("user", "critical", "rbac")
    @pytest.mark.api
    @pytest.mark.user
    @pytest.mark.negative
    @pytest.mark.critical
    @pytest.mark.rbac
    def test_negative_change_user(self, registered_user: ResponseTestUser, common_user: User):
        logger.info("Негативный тест. Попытка изменения пользователя без соответствующих прав")

        user_id = registered_user.id
        new_data = {"verified": True, "banned": False}
        common_user.api.user_api.change_user(user_id, new_data, expected_status=(403,))

    @allure.title("Негативный тест. Регистрация пользователя")
    @allure.tag("user", "critical", "rbac")
    @pytest.mark.api
    @pytest.mark.user
    @pytest.mark.negative
    @pytest.mark.critical
    @pytest.mark.rbac
    def test_get_user_by_id_common_user(self, common_user: User):
        # Попытка получения информации о пользователе без соответствующих прав
        common_user.api.user_api.get_user(common_user.email, expected_status=(403,))