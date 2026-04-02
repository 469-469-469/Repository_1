from typing import Union

import pytest
from tests.api.api_manager import ApiManagerAuth
import logging

logger = logging.getLogger(__name__)
MISSING = object()


class TestAuthAPIHappyPath:

    def test_register_and_login_user(self, api_manager_auth: ApiManagerAuth, registered_user: dict):
        # Регистрация и авторизация пользователя
        logger.info("Позитивный тест на регистрацию и авторизацию пользователя")
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }

        response = api_manager_auth.auth_api.login_user(login_data)
        response_data = response.json()

        # Проверки
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"

    def test_change_user(self, admin_api: ApiManagerAuth, registered_user: dict):
        # Изменение пользователя
        logger.info("Позитивный теста. Изменение пользователя")
        user_id = registered_user["id"]
        new_verified = True
        new_banned = False
        new_data = {"verified": new_verified, "banned": new_banned}

        response = admin_api.user_api.change_user(user_id, new_data, expected_status=200)
        response_data = response.json()

        # Проверки
        assert response_data["verified"] is new_verified, "Статус верификации не изменился"
        assert response_data["banned"] is new_banned, "Статус banned не изменился"


class TestAuthNegative:

    @pytest.mark.parametrize("field_register, value_register", [
        ("email", "abc"),         # некорректный email
        ("fullName", ""),         # пустая строка
        ("password", MISSING)     # ключ есть, но значение None
    ])
    def test_negative_register(self, api_manager_auth: ApiManagerAuth, test_user: dict, field_register: str,
                               value_register: Union[str, None, object]):
        # Регистрация пользователя
        logger.info(f"Негативный тест. Регистрация пользователя. Проверка поля {field_register}={value_register}")

        data = test_user.copy()
        if value_register is MISSING:
            data.pop(field_register, None)
        else:
            data[field_register] = value_register

        expected_status = 400
        api_manager_auth.auth_api.register_user(data, expected_status)

    @pytest.mark.parametrize("field_auth, value_auth", [
        ("email", "abc"),  # некорректный email
        ("email", ""),     # пустая строка
        ("password", "1"), # неверный пароль
        ("password", "")   # пустая строка
    ])
    def test_negative_auth(self, api_manager_auth: ApiManagerAuth, registered_user: dict, field_auth: str,
                           value_auth: Union[str, None, object]):
        # Авторизация пользователя
        logger.info(f"Негативный тест. Авторизация пользователя. Проверка поля {field_auth}={value_auth}")

        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }

        if value_auth is MISSING:
            login_data.pop(field_auth, None)
        else:
            login_data[field_auth] = value_auth

        expected_status = 401

        api_manager_auth.auth_api.login_user(login_data, expected_status)

    def test_negative_change_user(self, api_manager_auth: ApiManagerAuth, authorized_user: dict,
                                  registered_user: dict):
        # Попытка изменения пользователя без соответствующих прав
        logger.info("Негативный тест. Попытка изменения пользователя без соответствующих прав")

        user_id = registered_user["id"]
        new_data = {"verified": True, "banned": False}
        api_manager_auth.user_api.change_user(user_id, new_data, expected_status=403)