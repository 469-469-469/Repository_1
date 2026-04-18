from typing import Optional
import allure
from playwright.sync_api import expect, Page, Locator
from constants.constants import NEED_SCREENSHOT


class PageAction:
    """
    Базовые действия для всех страниц на сайте
    """
    def __init__(self, page: Page):
        self.button_name = None
        self.button_role = None
        self.home_url = "https://dev-cinescope.coconutqa.ru/"
        self.page = page
        self.url = None
        self.success_pop_up = None
        self.success_path = None

    @allure.step("Поиск элемента: locator={locator} role={role} name={name}")
    def get_locator(self, locator: str|None, role: str|None, name: str|None,placeholder: str|None) -> Optional[Locator]:
        if locator:
            return self.page.locator(locator)
        elif role and name:
            return self.page.locator("form").get_by_role(role, name=name)
        elif placeholder:
            return self.page.locator("form").get_by_placeholder(placeholder)
        else:
            raise ValueError("Передай locator или role+name")

    @allure.step("Переход на страницу: {url}")
    def open_url(self, url: str):
        self.page.goto(url)

    @allure.step("Ввод текста '{text}' в поле '{locator}'")
    def enter_text_to_element(self, locator: str|None = None, name: str|None = None, role: str|None = None,
                              placeholder: str|None = None,
                              text: str|None = None):
        self.get_locator(locator, role, name, placeholder).fill(text)

    @allure.step("Клик по элементу '{locator}'")
    def click_element(self, locator: str|None = None, role: str|None = None, name: str|None = None,
                      placeholder: str|None = None):
        self.get_locator(locator, role, name, placeholder).click()

    @allure.step("Ожидание загрузки страницы: {url}")
    def wait_redirect_for_url(self, url: str):
        expect(self.page).to_have_url(url)

    @allure.step("Получение текста элемента: {locator}")
    def get_element_text(self, locator: str|None = None, name: str|None = None, role: str|None = None,
                         placeholder: str|None = None) -> Optional[str]:
        return self.get_locator(locator, role, name, placeholder).text_content()

    @allure.step("Ожидание появления или исчезновения элемента: {locator}, state = {state}")
    def expect_visible(self, locator:str|None = None, name: str|None = None, role: str|None = None,
                       placeholder: str|None = None):
        expect(self.get_locator(locator, role, name, placeholder)).to_be_visible()

    @allure.step("Скриншот текущей страницы")
    def make_screenshot_and_attach_to_allure(self):
        screenshot = self.page.screenshot(full_page=True)
        allure.attach(screenshot, name="Screenshot", attachment_type=allure.attachment_type.PNG)

    @allure.step("Проверка наличия элемента с текстом: {text}")
    def check_element(self, locator:str|None = None, role: str|None = None, name: str|None = None,
                                placeholder: str|None = None):
        locator = self.get_locator(locator, role, name, placeholder)
        expect(locator).to_be_visible()

    @allure.step("Проверка всплывающего сообщения c текстом: {text}")
    def check_element_with_text(self, text: str):
        locator = self.page.get_by_text(text)
        expect(locator).to_be_visible()

class BasePage(PageAction): #
    """
    Базовая логика допустимая для всех страниц на сайте
    """
    def __init__(self, page: Page):
        super().__init__(page)

        # Общие локаторы для всех страниц на сайте
        self.button_name = None
        self.button_role = None
        self.home_button = "a[href='/' and text()='Cinescope']"
        self.all_movies_button = "a[href='/movies' and text()='Все фильмы']"

    @allure.step("Переход на главную страницу из шапки сайта")
    def go_to_home_page(self):
        self.click_element(self.home_button)
        self.wait_redirect_for_url(self.home_url)

    @allure.step("Переход на страницу 'Все фильмы из шапки сайта'")
    def go_to_all_movies(self):
        self.click_element(self.all_movies_button)
        self.wait_redirect_for_url(f"{self.home_url}movies")

    @allure.step("Контрольные проверки успешных действий")
    def success_check(self):
        self.wait_redirect_for_url(f"{self.home_url}{self.success_path}")
        if NEED_SCREENSHOT:
            self.make_screenshot_and_attach_to_allure()
        self.check_element_with_text(self.success_pop_up)

    @allure.step("Контрольные проверки отказа")
    def error_check(self):
        expect(self.page).to_have_url(f"{self.url}")
        if NEED_SCREENSHOT:
            self.make_screenshot_and_attach_to_allure()