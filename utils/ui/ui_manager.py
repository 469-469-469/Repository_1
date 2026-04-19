from utils.ui.auth_ui import RegisterPage, LoginPage
from utils.ui.review_ui import ReviewPage
from playwright.sync_api import Page


class UIManager:
    def __init__(self, page:Page):
        self.login_ui = LoginPage(page)
        self.register_ui = RegisterPage(page)
        self.review_ui = ReviewPage(page)
