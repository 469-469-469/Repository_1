import logging
from typing import Iterable

import requests

from constants.constants import LOGIN_ENDPOINT, REGISTER_ENDPOINT, LOGOUT_ENDPOINT, BASE_URL_AUTH
from custom_requester.custom_requester import CustomRequester

logger = logging.getLogger(__name__)


class AuthAPI(CustomRequester):

    """
      Класс для работы с аутентификацией.
    """

    def __init__(self, session:requests.Session):
        super().__init__(session=session, base_url=BASE_URL_AUTH)

    def register_user(self, user_data: dict, expected_status: Iterable[int] = (201,)):
        """
        Регистрация нового пользователя.
        :param user_data: Данные пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def login_user(self, login_data: dict, expected_status: Iterable[int] = (200,)):
        """
        Авторизация пользователя.
        :param login_data: Данные для логина.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    def authenticate(self, login_data: dict):
        response = self.login_user(login_data).json()

        if "accessToken" not in response:
            raise AssertionError("No accessToken in login response")

        token = response["accessToken"]

        # Сохраняем токен в User, если есть ссылка
        if hasattr(self, 'user'):
            self.user.token = token

        # Устанавливаем токен в CustomRequester, чтобы все запросы использовали Authorization
        self._update_session_headers(headers={"Authorization": f"Bearer {token}"})

        return token

    def logout(self):
        """
        Выход из аккаунта и очистка токена
        """
        # Делаем запрос на logout на сервере

        try:
            response = self.send_request(
                method="GET",
                endpoint=LOGOUT_ENDPOINT
            )
            # Убираем токен из заголовков после успешного выхода
            self.headers.pop("authorization", None)
            self.session.headers.pop("authorization", None)
            return response
        except (requests.exceptions.RequestException, ValueError) as e:
            logging.warning(f"Logout не удался: {e}")
            return None