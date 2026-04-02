import requests

from constants import BASE_URL_AUTH
from custom_requester.custom_requester import CustomRequester


class UserAPI(CustomRequester):

    """Класс для работы с API пользователей."""

    def __init__(self, session:requests.Session):
        super().__init__(session=session)
        self.session = session

    def get_user_info(self, user_id: int, expected_status: int = 200):
        """
        Получение информации о пользователе.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            base_url=BASE_URL_AUTH,
            endpoint=f"/user/{user_id}",
            expected_status=expected_status
        )

    def change_user(self, user_id: int, new_data: dict = None, expected_status: int = 200):
        """
        Получение информации о пользователе.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        :param new_data: На что меняются данные
        """
        return self.send_request(
            method="PATCH",
            base_url=BASE_URL_AUTH,
            endpoint=f"/user/{user_id}",
            data=new_data,
            expected_status=expected_status
        )

    def delete_user(self, user_id: int, expected_status: int = 204):
        """
        Удаление пользователя.
        :param user_id: ID пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            base_url=BASE_URL_AUTH,
            endpoint=f"/user/{user_id}",
            expected_status=expected_status
        )