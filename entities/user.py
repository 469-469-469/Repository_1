from models.creds_base_models import CredsModel, pydantic_user_creds
from utils.api.api_manager import ApiManager

class User:
    def __init__(self, email: str, password: str, roles: list, api: ApiManager):
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api
        self.token = None  # <-- сюда сохраним JWT после логина

    @property
    def creds(self) -> CredsModel:
        return pydantic_user_creds({"email": self.email, "password": self.password})

    def clear_tokens(self):
        self.token = None
        for api_client in [self.api.movies_api,
                           self.api.payment_api,
                           self.api.user_api]:
            if hasattr(api_client, "requester"):
                api_client.requester.headers.pop("Authorization", None)
                api_client.requester.session.headers.pop("Authorization", None)