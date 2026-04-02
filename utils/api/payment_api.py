from requests import Session

from constants import BASE_URL_PAYMENT
from custom_requester.custom_requester import CustomRequester


class PaymentAPI(CustomRequester):

    """Класс для работы с платежами."""

    def __init__(self, session: Session ):
        super().__init__(session=session)

    def get_user_id_payment(self, user_id: int, expected_status: int = 200):
        """
        Создание оплаты.
        :param user_id: Id пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            base_url=BASE_URL_PAYMENT,
            endpoint=f"/user/{user_id}",
            expected_status=expected_status
        )
