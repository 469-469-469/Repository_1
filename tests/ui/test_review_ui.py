import allure
import pytest
import logging
from entities.user import User
from models.movies_base_models import ResponseTestMovie
from faker import Faker
from utils.ui.base_classes import Locator, Checks
from utils.ui.ui_manager import UIManager

faker = Faker()
fake_ru = Faker("ru_RU")
logger = logging.getLogger(__name__)

@allure.epic("Cinescop")
@allure.feature("review_ui")
@allure.tag("positive")
class TestReviewUIHappyPath:

     @allure.title("Позитивный тест. Оставление отзыва")
     @allure.tag("regression", "review")
     @pytest.mark.ui
     @pytest.mark.review
     @pytest.mark.positive
     @pytest.mark.regression
     def test_create_review_ui(self, registered_user: User, ui: UIManager, movie: ResponseTestMovie):
         logger.info(f"Позитивный тест. Оставление отзыва на фильм с id: {movie.id}")

         with allure.step("Авторизация на сайте"):
             ui.login.login(registered_user.email, registered_user.password)
             ui.login.checks(Checks(path=ui.login.success_path, locator=ui.login.success_locator))

         ui.review.create_review(movie.id, fake_ru.sentence(nb_words=10))
         ui.review.checks(Checks(locator=ui.review.created_locator))

     @pytest.mark.skip(reason="Временно отключено из-за нестабильности локатора элемента")
     @allure.title("Позитивный тест. Удаление отзыва")
     @allure.tag("regression", "review", "fluky")
     @pytest.mark.ui
     @pytest.mark.review
     @pytest.mark.positive
     @pytest.mark.regression
     @pytest.mark.fluky
     def test_delete_review_ui(self, super_admin: User, ui: UIManager, movie_with_review: ResponseTestMovie):
         logger.info(f"Позитивный тест. Удаление отзыва на фильм с id: {movie_with_review.id}")

         with allure.step("Авторизация на сайте"):
             ui.login.login(super_admin.email, super_admin.password)
             ui.login.checks(Checks(path=ui.login.success_path, locator=ui.login.success_locator))

         ui.review.delete_review(movie_with_review.id)
         ui.review.checks(Checks(locator=ui.review.deleted_locator))


@allure.epic("Cinescop")
@allure.feature("review_ui")
@allure.tag("negative")
class TestReviewUINegative:

    @allure.title("Негативный тест. Оставление пустого отзыва")
    @allure.tag("regression", "review")
    @pytest.mark.ui
    @pytest.mark.review
    @pytest.mark.negative
    @pytest.mark.regression
    def test_empty_review_ui(self, registered_user: User, ui: UIManager, movie: ResponseTestMovie):
        logger.info(f"Негативный тест. Оставление пустого отзыва на фильм с id: {movie.id}")

        with allure.step("Авторизация на сайте"):
            ui.login.login(registered_user.email, registered_user.password)
            ui.login.checks(Checks(path=ui.login.success_path, locator=ui.login.success_locator))

        ui.review.create_review(movie.id, "")
        ui.review.checks(Checks(locator=Locator(text="Поле отзыва обязательно к заполнению")))


    @allure.title("Негативный тест. Удаление отзыва без аутентификации")
    @allure.tag("regression", "review")
    @pytest.mark.ui
    @pytest.mark.review
    @pytest.mark.negative
    @pytest.mark.regression
    def test_delete_review_ui(self, super_admin: User, ui: UIManager, movie_with_review: ResponseTestMovie):
        logger.info(f"Негативный тест. Удаление отзыва без аутентификации на фильм с id: {movie_with_review.id}")

        ui.review.delete_review(movie_with_review.id)
        ui.review.checks(Checks(locator=Locator(text="Произошла ошибка")))