import dataclasses
from typing import Optional
import allure
from playwright.sync_api import expect, Page, Locator
from constants.constants import NEED_SCREENSHOT


@dataclasses.dataclass
class ElementLocator:
    """
    Класс для хранения атрибутов поиска локатора
    """
    locator: str | None = None
    role: str|None = None
    name: str|None = None
    placeholder: str | None = None
    find_text: str | None = None


class PageAction:
    """
    Базовые действия для всех страниц на сайте
    """
    def __init__(self, page: Page):
        self.home_url = "https://dev-cinescope.coconutqa.ru/"
        self.page = page

    @allure.step("Поиск элемента")
    def locator(self, elements: ElementLocator):
        """
        Универсальный метод-локатор
        """
        locator = elements.locator
        role = elements.role
        name = elements.name
        placeholder = elements.placeholder
        find_text = elements.find_text

        if locator:
            return self.page.locator(locator)
        elif role and name:
            return self.page.locator("form").get_by_role(role, name=name)
        elif placeholder:
            return self.page.locator("form").get_by_placeholder(placeholder)
        elif find_text:
            return self.page.get_by_text(find_text)
        else:
            raise ValueError("Передай locator или role+name")

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
    def get_element_text(self,elements: ElementLocator) -> Optional[str]:
        return self.locator(elements).text_content()

    @allure.step("Ожидание появления или исчезновения элемента")
    def expect_visible(self, elements: ElementLocator):
        expect(self.locator(elements)).to_be_visible()

    @allure.step("Скриншот текущей страницы")
    def make_screenshot_and_attach_to_allure(self):
        screenshot = self.page.screenshot(full_page=True)
        allure.attach(screenshot, name="Screenshot", attachment_type=allure.attachment_type.PNG)

    @allure.step("Ожидание появления элемента с текстом")
    def wait_element(self,elements: ElementLocator):
        locator = self.locator(elements)
        expect(locator).to_be_visible()

    @allure.step("Проверка наличия элемента с текстом")
    def check_element(self, elements: ElementLocator):
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


    @allure.step("Переход на главную страницу из шапки сайта")
    def go_to_home_page(self):
        self.click(self.home_button)
        self.wait_redirect_for_url(self.home_url)

    @allure.step("Переход на страницу 'Все фильмы из шапки сайта'")
    def go_to_all_movies(self):
        self.click(self.all_movies_button)
        self.wait_redirect_for_url(f"{self.home_url}movies")

    @allure.step("Выход из аккаунта")
    def logout(self):
        self.click(self.profile)
        self.wait_redirect_for_url(f"{self.home_url}profile")
        self.click(self.exit)
        self.wait_element(self.enter)


    @allure.step("Контрольные проверки успешных действий")
    def success_check(self):
        self.wait_redirect_for_url(f"{self.home_url}{self.success_path}")
        if NEED_SCREENSHOT:
            self.make_screenshot_and_attach_to_allure()
        self.wait_element(elements=ElementLocator(find_text=self.success_pop_up))

    @allure.step("Контрольные проверки отказа")
    def error_check(self):
        with allure.step("Проверка нахождения на той же странице"):
            expect(self.page).to_have_url(f"{self.url}")
        if NEED_SCREENSHOT:
            self.make_screenshot_and_attach_to_allure()
