import allure
import pytest
from playwright.sync_api import Page
import logging
from models.users_base_models import RequestTestUser
from utils.ui.page_object_models import LoginPage, RegisterPage

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
     def test_register_ui(self, page: Page, creation_user_data: RequestTestUser):
         logger.info("Позитивный тест. Регистрация")

         register_page = RegisterPage(page)
         register_page.register(creation_user_data.fullName,creation_user_data.email,
                                creation_user_data.password)
         register_page.success_check()

     @allure.title("Позитивный тест. Авторизация пользователя")
     @allure.tag("smoke", "user")
     @pytest.mark.ui
     @pytest.mark.user
     @pytest.mark.positive
     @pytest.mark.smoke
     def test_login_ui(self, page: Page, registered_user: RequestTestUser):
         logger.info("Позитивный тест. Авторизация пользователя")

         login_page = LoginPage(page)
         login_page.login(registered_user.email, registered_user.password)
         login_page.success_check()


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
    @pytest.mark.parametrize("field_register, value_register", [
        ("email", "abc"),          # некорректный email
        ("fullName", ""),          # пустая строка
        ("password", "0123456789") # пароль не соответствует требованиям
    ])
    def test_register_ui(self, page: Page, creation_user_data: RequestTestUser, field_register: str,
                               value_register: str):
        logger.info(f"Негативный тест. Авторизация пользователя. Проверка поля {field_register}={value_register}")

        data = {"email": creation_user_data.email, "password": creation_user_data.password,
                      field_register: value_register}
        full_name = data.get("fullName", creation_user_data.fullName)
        email = data.get("email", creation_user_data.email)
        password = data.get("password", creation_user_data.password)

        register_page = RegisterPage(page)
        register_page.register(full_name, email, password)
        register_page.error_check()


    @allure.title("Негативный тест. Авторизация пользователя")
    @allure.tag("critical", "user")
    @pytest.mark.ui
    @pytest.mark.user
    @pytest.mark.negative
    @pytest.mark.critical
    @pytest.mark.parametrize("field_auth, value_auth", [
        pytest.param("email", "abc", marks=[pytest.mark.regression]),               # некорректный email
        pytest.param("email", "", marks=[pytest.mark.regression]),                  # пустая строка
        pytest.param("password", "", marks=[pytest.mark.rbac,pytest.mark.smoke]),   # пустая строка
        pytest.param("password", "1", marks=[pytest.mark.rbac,pytest.mark.smoke]),  # неверный пароль
    ])
    def test_login_ui(self, page: Page, registered_user: RequestTestUser, field_auth: str, value_auth: str):
        logger.info(f"Негативный тест. Авторизация пользователя. Проверка поля {field_auth}={value_auth}")

        login_data = {"email": registered_user.email, "password": registered_user.password,
                      field_auth: value_auth}
        login_page = LoginPage(page)
        login_page.login(login_data["email"], login_data["password"])
        login_page.error_check()