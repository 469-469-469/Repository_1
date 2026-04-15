from typing import Iterable
from constants import BASE_URL_AUTH

import requests
from custom_requester.custom_requester import CustomRequester


class UserAPI(CustomRequester):

    """Класс для работы с API пользователей."""

    def __init__(self, session:requests.Session):
        self.session = session
        super().__init__(session=session, base_url=BASE_URL_AUTH)
        self.requester = CustomRequester(session, base_url=BASE_URL_AUTH)

    def get_user(self, user_id: int,
                 expected_status: Iterable[int] = (200,)) -> requests.Response:
        """
        Получение информации о пользователе.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.requester.send_request(
            method="GET",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status
        )

    def create_user(self, user_data,
                    expected_status: Iterable[int] = (201,)) -> requests.Response:
        return self.requester.send_request(
            method="POST",
            endpoint="user",
            data=user_data,
            expected_status=expected_status
        )

    def change_user(self, user_id: int, new_data: dict = None,
                    expected_status: Iterable[int] = (200,)) -> requests.Response:
        """
        Получение информации о пользователе.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        :param new_data: На что меняются данные
        """
        return self.requester.send_request(
            method="PATCH",
            endpoint=f"/user/{user_id}",
            data=new_data,
            expected_status=expected_status
        )

    def delete_user(self, user_id: str,
                    expected_status: Iterable[int] = (204,)) -> requests.Response:
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.requester.send_request(
            method="DELETE",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status
        )