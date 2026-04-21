from playwright.sync_api import Page
from utils.ui.base_classes import BasePage, ElementLocator


class RegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}register"
        self.success_path = f"{self.home_url}login"

        self.success_locator = ElementLocator(find_text="Подтвердите свою почту")
        self.full_name_input = ElementLocator(locator="input[name='fullName']")
        self.email_placeholder = ElementLocator(placeholder="Email")
        self.password_input = ElementLocator(locator="input[name='password']")
        self.repeat_password_input = ElementLocator(locator="input[name='passwordRepeat']")
        self.button_register = ElementLocator(role="button", name="Зарегистрироваться")

    def register(self, full_name: str, email: str, password: str):
        self.open_url(self.url)
        self.fill(self.full_name_input,       text=full_name)
        self.fill(self.email_placeholder,     text=email)
        self.fill(self.password_input,        text=password)
        self.fill(self.repeat_password_input, text=password)
        self.click(self.button_register)


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}login"
        self.success_locator = ElementLocator(find_text="Вы вошли в аккаунт")
        self.success_path = self.home_url

        self.email_input = ElementLocator(locator="input[name='email']")
        self.password_input = ElementLocator(locator="input[name='password']")
        self.button_login = ElementLocator(role="button", name="Войти")

    def login(self, email: str, password: str):
        self.open_url(self.url)
        self.fill(self.email_input,    text=email)
        self.fill(self.password_input, text=password)
        self.click(self.button_login)


