import time
import allure
import pytest
from playwright.sync_api import sync_playwright
from utils.data_generator import DataGenerator
from utils.ui.page_object_models import LoginPage, RegisterPage


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
class TestLoginPage:
     @allure.title("Проведение успешного входа в систему")
     def test_login_by_ui(self, registered_user):
          with sync_playwright() as playwright:
               browser = playwright.chromium.launch(
                    headless=False)  # Запуск браузера headless=False для визуального отображения
               page = browser.new_page()
               login_page = LoginPage(page)  # Создаем объект страницы Login

               login_page.open()
               login_page.login(registered_user.email, registered_user.password)  # Осуществляем вход

               login_page.assert_was_redirect_to_home_page()  # Проверка редиректа на домашнюю страницу
               login_page.make_screenshot_and_attach_to_allure()  # Прикрепляем скриншот
               login_page.assert_alert_was_pop_up()  # Проверка появления и исчезновения алерта

               browser.close()


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Register")
@pytest.mark.ui
class TestRegisterPage:
     @allure.title("Проведение успешной регистрации")
     def test_register_by_ui(self):
          with sync_playwright() as playwright:
               # Подготовка данных для регистрации
               random_email = DataGenerator.generate_random_email()
               random_name = DataGenerator.generate_random_name()
               random_password = DataGenerator.generate_random_password()

               browser = playwright.chromium.launch(
                    headless=False)  # Запуск браузера headless=False для визуального отображения
               page = browser.new_page()

               register_page = RegisterPage(page)  # Создаем объект страницы регистрации cinescope
               register_page.open()
               register_page.register(f"PlaywrightTest {random_name}", random_email, random_password,
                                      random_password)  # Выполняем регистрацию

               register_page.assert_was_redirect_to_login_page()  # Проверка редиректа на страницу /login
               register_page.make_screenshot_and_attach_to_allure()  # Прикрепляем скриншот
               register_page.assert_alert_was_pop_up()  # Проверка появления и исчезновения алерта

               browser.close()
