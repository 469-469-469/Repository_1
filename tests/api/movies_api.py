from requests import Session
from constants import MOVIE_ENDPOINT, BASE_URL_MOVIES
from custom_requester.custom_requester import CustomRequester


class MoviesAPI(CustomRequester):

    """Класс для работы с фильмами."""

    def __init__(self, session:Session):
        super().__init__(session=session)

    def get_poster_movie(self, data_poster: dict, expected_status: int = 200):
        """
        Получение афиш фильмов.
        :param data_poster: Данные афиши.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            base_url=BASE_URL_MOVIES,
            endpoint=MOVIE_ENDPOINT,
            params=data_poster,
            expected_status=expected_status
        )

    def create_movie(self, data_movie: dict, expected_status: int = 201):
        """
        Создание нового фильма.
        :param data_movie: Данные фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            base_url=BASE_URL_MOVIES,
            endpoint=MOVIE_ENDPOINT,
            data=data_movie,
            expected_status=expected_status
        )

    def get_movie(self, id_movie: int, expected_status: int = 200):
        """
        Получение данных фильма.
        :param id_movie:  Id фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            base_url=BASE_URL_MOVIES,
            endpoint=f"{MOVIE_ENDPOINT}/{id_movie}",
            expected_status=expected_status
        )

    def change_movie(self, id_movie: int, data_movie: dict, expected_status: int = 200):
        """
        Редактирование фильма.
        :param id_movie:  Id фильма.
        :param data_movie: ОНовые данные фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="PATCH",
            base_url=BASE_URL_MOVIES,
            endpoint=f"{MOVIE_ENDPOINT}/{id_movie}",
            data=data_movie,
            expected_status=expected_status
        )

    def delete_movie(self, id_movie: int, expected_status: int = 200):
        """
        Удаление фильма.
        :param id_movie:  Id фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            base_url=BASE_URL_MOVIES,
            endpoint=f"{MOVIE_ENDPOINT}/{id_movie}",
            expected_status=expected_status
        )