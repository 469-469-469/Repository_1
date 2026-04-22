from playwright.sync_api import Page
from utils.ui.base_classes import BasePage, Locator
from faker import Faker
faker = Faker()
fake_ru = Faker("ru_RU")

class ReviewPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.deleted_locator = Locator(text="Отзыв успешно удален")
        self.created_locator = Locator(text="Отзыв успешно создан")
        self.review_input = Locator(role="textbox", name="Написать отзыв")
        self.review_send_button = Locator(role="button", name="Отправить")
        self.button_option = Locator(locator="div:has(h4:has-text('Жмышенко Валерий Альбертович')) button")
        self.button_delete = Locator(locator="[role='menuitem']:has-text('Удалить')")

    def create_review(self, movie_id: int, text_review: str):
        link_to_movie = f"{self.home_url}movies/{movie_id}"
        self.open_url(link_to_movie)
        self.wait_redirect_for_url(link_to_movie)
        self.fill(self.review_input, text=text_review)
        self.click(self.review_send_button)

    def delete_review(self, movie_id: int):
        self.open_url(f"{self.home_url}movies/{movie_id}")
        self.locator(self.button_option).wait_for(state="visible")
        self.click(self.button_option)
        self.locator(self.button_delete).wait_for(state="visible")
        self.click(self.button_delete)
