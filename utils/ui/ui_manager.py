from utils.ui.auth_ui import RegisterPage, LoginPage
from utils.ui.review_ui import ReviewPage
from playwright.sync_api import Page


class UIManager:
    def __init__(self, page: Page):
        self.login = LoginPage(page)
        self.register = RegisterPage(page)
        self.review = ReviewPage(page)
