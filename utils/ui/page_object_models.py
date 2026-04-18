from time import sleep

from playwright.sync_api import Page
from utils.ui.base_classes import BasePage, ElementLocator


class RegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}register"
        self.success_pop_up = "Подтвердите свою почту"
        self.success_path = "login"

        self.full_name_input = ElementLocator(locator="input[name='fullName']")
        self.email_placeholder = ElementLocator(placeholder="Email")
        self.password_input = "input[name='password']"
        self.repeat_password_input = "input[name='passwordRepeat']"
        self.button_role = "button"
        self.button_name = "Зарегистрироваться"

        self.open_url(self.url)

    def register(self, full_name: str, email: str, password: str):
        self.fill(self.full_name_input, text=full_name)
        self.fill(self.email_placeholder, text=email)
        self.fill(ElementLocator(locator=self.password_input),        text=password)
        self.fill(ElementLocator(locator=self.repeat_password_input), text=password)
        self.click(ElementLocator(role=self.button_role, name=self.button_name))


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
        self.fill(ElementLocator(locator=self.password_input),  text=password)
        self.fill(ElementLocator(locator=self.email_input),     text=email)
        self.click(ElementLocator(role=self.button_role, name=self.button_name))