from playwright.sync_api import Page
from utils.ui.base_classes import BasePage, Locator


class RegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}register"
        self.success_path = f"{self.home_url}login"

        self.success_locator = Locator(text="Подтвердите свою почту")
        self.full_name_input = Locator(locator="input[name='fullName']")
        self.email_placeholder = Locator(placeholder="Email")
        self.password_input = Locator(locator="input[name='password']")
        self.repeat_password_input = Locator(locator="input[name='passwordRepeat']")
        self.button_register = Locator(role="button", name="Зарегистрироваться")

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
        self.success_locator = Locator(text="Вы вошли в аккаунт")
        self.success_path = self.home_url

        self.email_input = Locator(locator="input[name='email']")
        self.password_input = Locator(locator="input[name='password']")
        self.button_login = Locator(role="button", name="Войти")

    def login(self, email: str, password: str):
        self.open_url(self.url)
        self.fill(self.email_input,    text=email)
        self.fill(self.password_input, text=password)
        self.click(self.button_login)


