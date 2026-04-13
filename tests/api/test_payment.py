import pytest
import allure
from entities.user import User
import logging
import pytest_check as check
from utils.auto_step_class import auto_step_class
from models.users_base_models import ResponseTestUser

logger = logging.getLogger(__name__)

@allure.epic("Cinescop")
@allure.feature("payment_api")
@allure.tag("positive")
@auto_step_class
class TestPaymentAPIHappyPath:

    @allure.title("Получение платежей пользователя")
    @allure.tag("smoke", "payment")
    @pytest.mark.api
    @pytest.mark.payment
    @pytest.mark.positive
    @pytest.mark.smoke
    def test_get_user_payment(self, super_admin: User, registered_user: ResponseTestUser):
        logger.info("Позитивный тест. Получение платежей пользователя")

        user_id = registered_user.id
        response = super_admin.api.payment_api.get_user_id_payment(user_id)
        response_data = response.json()

        required_fields = [
            "amount",
            "id",
            "userId",
            "movieId",
            "status",
            "total",
            "createdAt",
        ]
        if not response_data:
            logger.info("Оплат не найдено")
            return
        for field in required_fields:
            check.is_in(field, response_data[0], f"В ответе нет поля '{field}'")
