from playwright.sync_api import Page
from utils.ui.base_classes import BasePage, ElementLocator
from faker import Faker
faker = Faker()
fake_ru = Faker("ru_RU")

class ReviewPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.success_pop_up = "Отзыв успешно удален"
        self.review_input = ElementLocator(role="textbox", name="Написать отзыв")
        self.review_send_button = ElementLocator(role="button", name="Отправить")
        self.button_option = ElementLocator(locator="div:has(h4:has-text('Жмышенко Валерий Альбертович')) button")
        self.button_delete = ElementLocator(locator="[role='menuitem']:has-text('Удалить')")