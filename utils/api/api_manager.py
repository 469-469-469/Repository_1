from requests import Session

from utils.api.auth_api import AuthAPI
from utils.api.payment_api import PaymentAPI
from utils.api.user_api import UserAPI
from utils.api.movies_api import MoviesAPI


class ApiManagerAuth:

    """Класс для управления API-классами с единой HTTP-сессией."""

    def __init__(self, session:Session):
        """
        Инициализация ApiManagerAuth.
        :param session: HTTP-сессия, используемая всеми API-классами.
        """
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session)


class ApiManagerMovies:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """
    def __init__(self, session:Session):
        """
        Инициализация ApiManagerMovies.
        :param session: HTTP-сессия, используемая всеми API-классами.
        """
        self.session = session
        self.movies_api = MoviesAPI(session)
        self.auth_api = AuthAPI(session)


class ApiManagerPayment:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """
    def __init__(self, session:Session):
        """
        Инициализация ApiManagerPayment.
        :param session: HTTP-сессия, используемая всеми API-классами.
        """
        self.session = session
        self.payment_api = PaymentAPI(session)
        self.auth_api = AuthAPI(session)

