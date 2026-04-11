from requests import Session

from utils.api.auth_api import AuthAPI
from utils.api.payment_api import PaymentAPI
from utils.api.user_api import UserAPI
from utils.api.movies_api import MoviesAPI

class ApiManager:
    def __init__(self, session: Session):
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session)
        self.movies_api = MoviesAPI(session)
        self.payment_api = PaymentAPI(session)

    def close_session(self):
        self.auth_api.session.close()