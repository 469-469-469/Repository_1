from time import sleep
import allure
import pytest
import logging
from entities.user import User
from models.movies_base_models import ResponseTestMovie
from faker import Faker
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
     def test_leaving_review_ui(self, registered_user: User, page: UIManager, movie: ResponseTestMovie):
         logger.info("Позитивный тест. Оставление отзыва")

         review = page.review_ui
         login =  page.login_ui

         login.login(registered_user.email, registered_user.password)
         login.success_check()

         link_to_movie = f"{review.home_url}movies/{movie.id}"
         text_review = fake_ru.sentence(nb_words=10)
         review.open_url(link_to_movie)
         review.wait_redirect_for_url(link_to_movie)
         review.fill(review.review_input, text=text_review)
         review.click(review.review_send_button)

     @allure.title("Позитивный тест. Удаление отзыва")
     @allure.tag("regression", "review", "fluky")
     @pytest.mark.ui
     @pytest.mark.review
     @pytest.mark.positive
     @pytest.mark.regression
     @pytest.mark.fluky
     def test_delete_review_ui(self, super_admin: User, page: UIManager, movie_with_review: ResponseTestMovie):
         logger.info("Позитивный тест. Удаление отзыва")

         review = page.review_ui
         login = page.login_ui

         login.login(super_admin.email, super_admin.password)
         login.success_check()

         review.delete_review(movie_with_review.id)
         review.success_check(success_path=False, success_popup=True)


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
    def test_empty_review_ui(self, registered_user: User, page: UIManager, movie: ResponseTestMovie):
        logger.info("Негативный тест. Оставление пустого отзыва")

        error_text = "Поле отзыва обязательно к заполнению"
        review = page.review_ui
        login =  page.login_ui

        login.login(registered_user.email, registered_user.password)
        login.success_check()

        link_to_movie = f"{review.home_url}movies/{movie.id}"
        review.open_url(link_to_movie)
        review.wait_redirect_for_url(link_to_movie)
        review.fill(review.review_input, text="")
        review.click(review.review_send_button)
        review.error_check(error_path=False, error_text=error_text)
        sleep(3)


    @allure.title("Негативный тест. Удаление отзыва без аутентификации")
    @allure.tag("regression", "review")
    @pytest.mark.ui
    @pytest.mark.review
    @pytest.mark.negative
    @pytest.mark.regression
    def test_delete_review_ui(self, super_admin: User, page: UIManager, movie_with_review: ResponseTestMovie):
        logger.info("Негативный тест. Удаление отзыва без аутентификации")

        error_text = "Произошла ошибка"
        review = page.review_ui
        review.delete_review(movie_with_review.id)
        review.error_check(error_path=False, error_text=error_text)



