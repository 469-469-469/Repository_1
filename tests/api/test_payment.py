from tests.api.api_manager import ApiManagerPayment, ApiManagerAuth
from faker import Faker
import logging

logger = logging.getLogger(__name__)


class TestPaymentAPIHappyPath:

    def test_get_user_payment(self, admin_api: ApiManagerAuth, registered_user: dict,
                              api_manager_payment:ApiManagerPayment):
        # Получение платежей пользователя
        logger.info("Позитивный тест. Получение платежей пользователя")

        user_id = registered_user["id"]
        response = api_manager_payment.payment_api.get_user_id_payment(user_id)
        response_data = response.json()

        # Проверки
        if response_data:
            assert "id" in response_data[0]
            assert "userId" in response_data[0]
            assert "movieId" in response_data[0]
            assert "status" in response_data[0]
            assert "amount" in response_data[0]
            assert "total" in response_data[0]
            assert "createdAt" in response_data[0]
        else:
            logger.info("Оплат не найдено")

