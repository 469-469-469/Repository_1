import dataclasses
from typing import Optional
import allure
from playwright.sync_api import expect, Page
from constants.constants import NEED_SCREENSHOT


@dataclasses.dataclass
class Locator:
    """
    Класс с атрибутами поиска элемента (для универсального метода-локатора)
    """
    locator: str | None = None
    path: str | None = None
    role: str | None = None
    name: str | None = None
    placeholder: str | None = None
    text: str | None = None


@dataclasses.dataclass
class Checks:
    """
    Класс с атрибутами финальной проверки
    """
    path: str | None = None
    locator: Locator | None = None
    text: str | None = None
    name: str | None = None


class PageAction:
    """
    Базовые действия для всех страниц на сайте
    """
    def __init__(self, page: Page):
        self.home_url = "https://dev-cinescope.coconutqa.ru/"
        self.page = page

    def locator(self, elements: Locator):
        """
        Универсальный метод-локатор
        """
        locator = elements.locator
        role = elements.role
        name = elements.name
        placeholder = elements.placeholder
        find_text = elements.text

        if locator:
            return self.page.locator(locator)

        if role and name:
            return self.page.locator("form").get_by_role(role, name=name)

        if placeholder:
            return self.page.locator("form").get_by_placeholder(placeholder)

        if find_text:
            return self.page.get_by_text(find_text)

        raise ValueError("Передайте данные для поиска элемента")

    @allure.step("Финальные проверки")
    def checks(self, checks: Checks):
        errors = []
        if checks.path:
            try:
                self.wait_redirect_for_url(checks.path)
            except AssertionError as e:
                errors.append(str(e))
        if checks.locator:
            try:
                self.expect_visible(checks.locator)
            except AssertionError as e:
                errors.append(str(e))
        if checks.text:
            try:
                self.check_contain_text(checks.text)
            except AssertionError as e:
                errors.append(str(e))

        self.make_screenshot_to_allure()

        if errors:
            raise AssertionError("\n".join(errors))

    @allure.step("Переход на страницу")
    def open_url(self, url: str):
        self.page.goto(url)

    @allure.step("Ввод текста")
    def fill(self, elements: Locator, text: str):
        self.locator(elements).fill(text)

    @allure.step("Клик по элементу")
    def click(self, elements: Locator):
        self.locator(elements).click()

    @allure.step("Проверка наличия элемента с текстом")
    def check_visible(self, elements: Locator) -> bool:
        return self.locator(elements).is_visible()

    @allure.step("Ожидание загрузки страницы")
    def wait_redirect_for_url(self, url: str):
        expect(self.page).to_have_url(url)

    @allure.step("Получение текста элемента")
    def get_element_text(self, elements: Locator) -> Optional[str]:
        return self.locator(elements).text_content()

    @allure.step("Ожидание появления элемента")
    def expect_visible(self, elements: Locator):
        expect(self.locator(elements)).to_be_visible()

    @allure.step("Ожидание появления элемента, содержащего текст")
    def check_contain_text(self, text) -> bool:
        return expect(self.page.locator("form")).to_contain_text(text)

    def make_screenshot_to_allure(self):
        if NEED_SCREENSHOT:
            screenshot = self.page.screenshot(full_page=True)
            allure.attach(screenshot, name="Скриншот текущей страницы", attachment_type=allure.attachment_type.PNG)


class BasePage(PageAction): #
    """
    Базовая логика, допустимая для всех страниц на сайте
    """
    def __init__(self, page: Page):
        super().__init__(page)

        # Общие локаторы для всех страниц на сайте
        self.home_button = Locator(locator="xpath=//a[@href='/' and text()='Cinescope']")
        self.all_movies_button = Locator(locator="xpath=//a[@href='/movies' and text()='Все фильмы']")
        self.enter = Locator(role="button", name="Войти")
        self.profile = Locator(locator="button:has-text('Профиль')")
        self.exit = Locator(locator="button:has-text('Выход')")

    @allure.step("Переход на главную страницу из хедера сайта")
    def go_to_home_page(self):
        self.click(self.home_button)
        self.wait_redirect_for_url(self.home_url)

    @allure.step("Переход на страницу 'Все фильмы из хедера сайта'")
    def go_to_all_movies(self):
        self.click(self.all_movies_button)
        self.wait_redirect_for_url(f"{self.home_url}movies")
