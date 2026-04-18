from playwright.async_api import Page
from utils.ui.base_classes import BasePage


class RegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}register"
        self.success_pop_up = "Подтвердите свою почту"
        self.success_path = "login"

        self.full_name_input = "input[name='fullName']"
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.repeat_password_input = "input[name='passwordRepeat']"
        self.button_role = "button"
        self.button_name = "Зарегистрироваться"

        self.open_url(self.url)

    def register(self, full_name: str, email: str, password: str):
        self.enter_text_to_element(self.full_name_input, full_name)
        self.enter_text_to_element(self.email_input, email)
        self.enter_text_to_element(self.password_input, password)
        self.enter_text_to_element(self.repeat_password_input, password)
        self.click_element(None, self.button_role, self.button_name)

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}login"
        self.success_pop_up = "Вы вошли в аккаунт"
        self.success_path = ""

        self.open_url(self.url)

        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.button_role = "button"
        self.button_name = "Войти"

    def login(self, email: str, password: str):
        self.enter_text_to_element(self.password_input, password)
        self.enter_text_to_element(self.email_input, email)
        self.click_element(None, self.button_role, self.button_name)