import allure
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
     def test_register_by_ui(self, page: Page, creation_user_data: RequestTestUser):
         logger.info("Позитивный тест. Регистрация")

         register_page = RegisterPage(page)
         register_page.register(creation_user_data.fullName,creation_user_data.email,
                                creation_user_data.password)
         register_page.success_check(True, True, True)

     @allure.title("Позитивный тест. Вход в систему")
     def test_login_by_ui(self, page: Page, registered_user: RequestTestUser):
         logger.info("Позитивный тест. Вход в систему")

         login_page = LoginPage(page)
         login_page.login(registered_user.email, registered_user.password)
         login_page.success_check(True, True, True)