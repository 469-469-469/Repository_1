from typing import Optional

import allure
from playwright.sync_api import expect, Page


class PageAction:

    """Класс для ."""

    def __init__(self, page: Page):
        self.home_url = "https://dev-cinescope.coconutqa.ru/"
        self.page = page
        self.url = None
        self.success_pop_up = None
        self.success_path = None

    @allure.step("Переход на страницу: {url}")
    def open_url(self, url: str):
        self.page.goto(url)

    @allure.step("Ввод текста '{text}' в поле '{locator}'")
    def enter_text_to_element(self, locator: str, text: str):
        self.page.fill(locator, text)

    @allure.step("Клик по элементу '{locator}'")
    def click_element(self, locator: str):
        self.page.click(locator)

    @allure.step("Ожидание загрузки страницы: {url}")
    def wait_redirect_for_url(self, url: str):
        expect(self.page).to_have_url(url)

    @allure.step("Получение текста элемента: {locator}")
    def get_element_text(self, locator: str) -> Optional[str]:
        return self.page.locator(locator).text_content()

    @allure.step("Ожидание появления или исчезновения элемента: {locator}, state = {state}")
    def expect_visible(self, locator: str) -> None:
        expect(self.page.locator(locator)).to_be_visible()

    @allure.step("Скриншот текущей страницы")
    def make_screenshot_and_attach_to_allure(self):
        screenshot = self.page.screenshot(full_page=True)
        allure.attach(screenshot, name="Screenshot", attachment_type=allure.attachment_type.PNG)

    @allure.step("Проверка всплывающего сообщения c текстом: {text}")
    def check_pop_up_element_with_text(self, text: str):
        locator = self.page.get_by_text(text)

        expect(locator).to_be_visible()
        locator.wait_for(state="hidden")


class BasePage(PageAction): #Базовая логика допустимая для всех страниц на сайте

    """Класс для ."""

    def __init__(self, page: Page):
        super().__init__(page)

        # Общие локаторы для всех страниц на сайте
        self.home_button = "a[href='/' and text()='Cinescope']"
        self.all_movies_button = "a[href='/movies' and text()='Все фильмы']"

    @allure.step("Открытие страницы")
    def open(self):
        self.open_url(self.url)

    @allure.step("Переход на главную страницу из шапки сайта")
    def go_to_home_page(self):
        self.click_element(self.home_button)
        self.wait_redirect_for_url(self.home_url)

    @allure.step("Переход на страницу 'Все фильмы из шапки сайта'")
    def go_to_all_movies(self):
        self.click_element(self.all_movies_button)
        self.wait_redirect_for_url(f"{self.home_url}movies")

    @allure.step("Контрольные проверки")
    def success_check(self, check_final_page: bool = False, need_screenshot: bool = False,
                      check_pop_up: bool = False):
        if check_final_page:
            self.wait_redirect_for_url(f"{self.home_url}{self.success_path}")
        if need_screenshot:
            self.make_screenshot_and_attach_to_allure()
        if check_pop_up:
            self.check_pop_up_element_with_text(self.success_pop_up)