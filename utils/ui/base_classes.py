import dataclasses
from typing import Optional
import allure
from playwright.sync_api import expect, Page
from constants.constants import NEED_SCREENSHOT


@dataclasses.dataclass
class ElementLocator:
    """
    Класс для хранения атрибутов поиска элемента
    """
    locator: str | None = None
    path: str | None = None
    role: str | None = None
    name: str | None = None
    placeholder: str | None = None
    find_text: str | None = None


@dataclasses.dataclass
class FinalChecks:
    """
    Класс для хранения атрибутов финальных проверок
    """
    path: str | None = None
    locator: ElementLocator | None = None
    error: str | None = None
    name: str | None = None


class PageAction:
    """
    Базовые действия для всех страниц на сайте
    """
    def __init__(self, page: Page):
        self.home_url = "https://dev-cinescope.coconutqa.ru/"
        self.page = page

    def locator(self, elements: ElementLocator):
        """
        Универсальный метод-локатор
        """
        locator = elements.locator
        role = elements.role
        name = elements.name
        placeholder = elements.placeholder
        find_text = elements.find_text

        match True:
            case _ if locator:
                return self.page.locator(locator)
            case _ if role and name:
                return self.page.locator("form").get_by_role(role, name=name)
            case _ if placeholder:
                return self.page.locator("form").get_by_placeholder(placeholder)
            case _ if find_text:
                return self.page.get_by_text(find_text)
            case _:
                raise ValueError("Передайте данные для поиска элемента")

    @allure.step("Переход на страницу")
    def open_url(self, url: str):
        self.page.goto(url)

    @allure.step("Ввод текста")
    def fill(self, elements: ElementLocator, text: str):
        self.locator(elements).fill(text)

    @allure.step("Клик по элементу")
    def click(self, elements: ElementLocator):
        self.locator(elements).click()

    @allure.step("Ожидание загрузки страницы")
    def wait_redirect_for_url(self, url: str):
        expect(self.page).to_have_url(url)

    @allure.step("Получение текста элемента")
    def get_element_text(self, elements: ElementLocator) -> Optional[str]:
        return self.locator(elements).text_content()

    @allure.step("Ожидание появления элемента")
    def expect_visible(self, elements: ElementLocator):
        expect(self.locator(elements)).to_be_visible()

    @allure.step("Скриншот текущей страницы")
    def make_screenshot_and_attach_to_allure(self):
        if NEED_SCREENSHOT:
            screenshot = self.page.screenshot(full_page=True)
            allure.attach(screenshot, name="Screenshot", attachment_type=allure.attachment_type.PNG)

    @allure.step("Проверка наличия элемента с текстом")
    def check_element(self, elements: ElementLocator) -> bool:
        return self.locator(elements).is_visible()


class BasePage(PageAction): #
    """
    Базовая логика допустимая для всех страниц на сайте
    """
    def __init__(self, page: Page):
        super().__init__(page)

        # Общие локаторы для всех страниц на сайте
        self.home_button = ElementLocator(locator="xpath=//a[@href='/' and text()='Cinescope']")
        self.all_movies_button = ElementLocator(locator="xpath=//a[@href='/movies' and text()='Все фильмы']")
        self.enter = ElementLocator(role="button", name="Войти")
        self.profile = ElementLocator(locator="button:has-text('Профиль')")
        self.exit = ElementLocator(locator="button:has-text('Выход')")

    @allure.step("Переход на главную страницу из хедера сайта")
    def go_to_home_page(self):
        self.click(self.home_button)
        self.wait_redirect_for_url(self.home_url)

    @allure.step("Переход на страницу 'Все фильмы из хедера сайта'")
    def go_to_all_movies(self):
        self.click(self.all_movies_button)
        self.wait_redirect_for_url(f"{self.home_url}movies")

    @allure.step("Контрольные проверки")
    def final_checks(self, elements: FinalChecks):
        if elements.path:
            with allure.step("Проверка нахождения на корректной странице"):
                expect(self.page).to_have_url(elements.path)
        if elements.locator:
            with allure.step("Проверка появления элемента с сообщением об ошибке"):
                self.expect_visible(elements=elements.locator)
        if elements.error:
            with allure.step("Проверка появления текста сообщения об ошибке"):
                expect(self.page.locator("form")).to_contain_text(elements.error)
        self.make_screenshot_and_attach_to_allure()
