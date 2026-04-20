import allure
import pytest
import logging
from models.users_base_models import RequestTestUser
from utils.ui.base_classes import FinalChecks
from utils.ui.ui_manager import UIManager

logger = logging.getLogger(__name__)

@allure.epic("Cinescop")
@allure.feature("auth_ui")
@allure.tag("positive")
class TestAuthUIHappyPath:

     @allure.title("Позитивный тест. Регистрация")
     @allure.tag("smoke", "user")
     @pytest.mark.ui
     @pytest.mark.user
     @pytest.mark.positive
     @pytest.mark.smoke
     def test_register_ui(self, ui: UIManager, creation_user_data: RequestTestUser):
         logger.info("Позитивный тест. Регистрация")

         ui.register.register(creation_user_data.fullName, creation_user_data.email, creation_user_data.password)
         ui.register.final_checks(FinalChecks(path=ui.register.success_path, locator=ui.register.success_locator))


     @allure.title("Позитивный тест. Авторизация пользователя")
     @allure.tag("smoke", "user")
     @pytest.mark.ui
     @pytest.mark.user
     @pytest.mark.positive
     @pytest.mark.smoke
     def test_login_ui(self, ui: UIManager, registered_user: RequestTestUser):
         logger.info("Позитивный тест. Авторизация пользователя")

         ui.login.login(registered_user.email, registered_user.password)
         ui.login.final_checks(FinalChecks(path=ui.login.success_path, locator=ui.login.success_locator))


@allure.epic("Cinescop")
@allure.feature("auth_ui")
@allure.tag("negative")
class TestAuthUINegative:
    @allure.title("Негативный тест. Регистрация")
    @allure.tag("regression", "user")
    @pytest.mark.ui
    @pytest.mark.user
    @pytest.mark.negative
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "field, value, expected_error",
        [
            ("password", "0123456789", "Пароль не соответствует требованиям"),
            ("email", "", "Неверная почта"),
            ("fullName", "", None),
        ]
    )
    def test_register_ui(self, ui: UIManager, creation_user_data: RequestTestUser, field: str,
                               value: str, expected_error: str | None):
        logger.info(f"Негативный тест. Регистрация. Проверка поля {field}={value}")

        data = {"email": creation_user_data.email, "password": creation_user_data.password, field: value}
        full_name = data.get("fullName", creation_user_data.fullName)
        email = data.get("email", creation_user_data.email)
        password = data.get("password", creation_user_data.password)

        ui.register.register(full_name, email, password)
        ui.register.final_checks(FinalChecks(path=ui.register.url, error=expected_error))


    @allure.title("Негативный тест. Авторизация")
    @allure.tag("critical", "user")
    @pytest.mark.ui
    @pytest.mark.user
    @pytest.mark.negative
    @pytest.mark.critical
    @pytest.mark.parametrize(
        "field, value, expected_error",
        [
            ("email", "", "Поле email не может быть пустым"),
            ("password", "", "Поле пароль не может быть пустым"),
            ("password", "1", None) # Неверный пароль
        ]
    )
    def test_login_ui(self, ui: UIManager, registered_user: RequestTestUser, field: str, value: str,
                      expected_error: str | None):
        logger.info(f"Негативный тест. Авторизация. Проверка поля {field}={value}")

        login_data = {"email": registered_user.email, "password": registered_user.password, field: value}
        ui.login.login(login_data["email"], login_data["password"])
        ui.login.final_checks(FinalChecks(path=ui.login.url, error=expected_error))