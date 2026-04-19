from time import sleep

from playwright.sync_api import Page
from utils.ui.base_classes import BasePage, ElementLocator

class ReviewPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.review_input = ElementLocator(role="textbox", name="Написать отзыв")
        self.review_send_button = ElementLocator(role="button", name="Отправить")