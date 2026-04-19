from time import sleep

import allure
import pytest
import logging

from entities.user import User
from models.movies_base_models import ResponseTestMovie
from models.users_base_models import ResponseTestUser
from faker import Faker
from playwright.sync_api import Page
from utils.ui.review_ui import ReviewPage
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
     def test_leaving_a_review_ui(self, registered_user: User, page: UIManager, movie: ResponseTestMovie):
         logger.info("Позитивный тест. Оставление отзыва")

         review = page.review_ui
         login =  page.login_ui

         login.login(registered_user.email, registered_user.password)
         login.success_check()
         link_to_movie = f"{review.home_url}movies/{movie.id}"
         text_review = fake_ru.sentence(nb_words=10)
         review.open_url(link_to_movie)
         review.wait_redirect_for_url(link_to_movie)
         review.fill(review.review_input,    text=text_review)

         review.click(review.review_send_button)
         sleep(3)


class TestReviewUINegative:
    pass