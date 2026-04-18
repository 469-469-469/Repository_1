# constants.py
BASE_URL_AUTH = "https://auth.dev-cinescope.coconutqa.ru"
BASE_URL_MOVIES = "https://api.dev-cinescope.coconutqa.ru"
BASE_URL_PAYMENT = "https://payment.dev-cinescope.coconutqa.ru"


HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"
LOGOUT_ENDPOINT = "/logout"

MOVIE_ENDPOINT = "/movies"
USER_ENDPOINT = "/user"

PAYMENT_CREATE_ENDPOINT = "/create"

GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'


DEFAULT_UI_TIMEOUT = 30000  # 30 секунд

NEED_SCREENSHOT = True