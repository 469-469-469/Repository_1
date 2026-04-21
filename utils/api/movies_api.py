from typing import Iterable

import requests
from requests import Session
from constants.constants import MOVIE_ENDPOINT, BASE_URL_MOVIES, REVIEW_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from models.movies_base_models import RequestTestMovie
from models.posters_base_models import RequestTestPoster


class MoviesAPI(CustomRequester):

    """Класс для работы с фильмами."""

    def __init__(self, session:Session):
        super().__init__(session=session, base_url=BASE_URL_MOVIES)
        self.requester = CustomRequester(session, base_url=BASE_URL_MOVIES)

    def get_poster_movie(self, data_poster: RequestTestPoster,
                         expected_status: Iterable[int] = (200,)) -> requests.Response:
        """
        Получение афиш фильмов.
        :param data_poster: Данные афиши.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=MOVIE_ENDPOINT,
            params=data_poster,
            expected_status=expected_status
        )

    def create_movie(self, data_movie: RequestTestMovie,
                     expected_status: Iterable[int] = (201,)) -> requests.Response:
        """
        Создание нового фильма.
        :param data_movie: Данные фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.requester.send_request(
            method="POST",
            endpoint=MOVIE_ENDPOINT,
            data=data_movie,
            expected_status=expected_status
        )

    def get_movie(self, id_movie: int,
                  expected_status: Iterable[int] = (200,)) -> requests.Response:
        """
        Получение данных фильма.
        :param id_movie:  Id фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.requester.send_request(
            method="GET",
            endpoint=f"{MOVIE_ENDPOINT}/{id_movie}",
            expected_status=expected_status
        )

    def change_movie(self, id_movie: int, data_movie: RequestTestMovie,
                     expected_status: Iterable[int] = (200,)) -> requests.Response:
        """
        Редактирование фильма.
        :param id_movie:  Id фильма.
        :param data_movie: Новые данные фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.requester.send_request(
            method="PATCH",
            endpoint=f"{MOVIE_ENDPOINT}/{id_movie}",
            data=data_movie,
            expected_status=expected_status
        )

    def delete_movie(self, id_movie: int,
                     expected_status: Iterable[int] = (200,)) -> requests.Response:
        """
        Удаление фильма.
        :param id_movie:  Id фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.requester.send_request(
            method="DELETE",
            endpoint=f"{MOVIE_ENDPOINT}/{id_movie}",
            expected_status=expected_status
        )

    def create_review(self, id_movie: int, rating: int, text: str,
                     expected_status: Iterable[int] = (201,)) -> requests.Response:
        """
        Создание отзыва.
        :param rating:
        :param text:
        :param id_movie:  Id фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        data_review = {
            "rating": rating,
            "text": text
        }
        return self.requester.send_request(
            method="POST",
            endpoint=f"{MOVIE_ENDPOINT}/{id_movie}{REVIEW_ENDPOINT}",
            data=data_review,
            expected_status=expected_status
        )