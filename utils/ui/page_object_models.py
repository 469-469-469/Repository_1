from playwright.async_api import Page
from utils.ui.base_classes import BasePage


class RegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}register"
        self.success_pop_up = "Подтвердите свою почту"
        self.success_path = "login"

        # Локаторы элементов
        self.full_name_input = "input[name='fullName']"
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.repeat_password_input = "input[name='passwordRepeat']"

        self.register_button = page.get_by_role("button", name="Зарегистрироваться")
        self.sign_button = "a[href='/login' and text()='Войти']"
        self.open_url(self.url)

        # Локальные action методы
    def register(self, full_name: str, email: str, password: str):
        self.enter_text_to_element(self.full_name_input, full_name)
        self.enter_text_to_element(self.email_input, email)
        self.enter_text_to_element(self.password_input, password)
        self.enter_text_to_element(self.repeat_password_input, password)
        self.register_button.click()

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}login"
        self.success_pop_up = "Вы вошли в аккаунт"
        self.success_path = ""
        self.open_url(self.url)

        # Локаторы элементов
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.login_button = page.locator("form").get_by_role("button", name="Войти")
        self.register_button = "a[href='/register' and text()='Зарегистрироваться']"

    # Локальные action методы
    def login(self, email: str, password: str):
        self.enter_text_to_element(self.password_input, password)
        self.enter_text_to_element(self.email_input, email)
        self.login_button.click()