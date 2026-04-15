import json
import logging
import os
from typing import Dict, Iterable

import allure
from pydantic import BaseModel
from typing_extensions import Unpack

import requests
from typing_extensions import TypedDict

from constants.constants import GREEN, RESET, RED


class HeadersKwargs(TypedDict, total=False):
    headers: Dict[str, str]


class CustomRequester:

    """Кастомный реквестер для стандартизации и упрощения отправки HTTP-запросов."""

    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, session: requests.Session, base_url: str, timeout: float = 10):
        self.session = session
        self.timeout = timeout
        self.headers = self.base_headers.copy()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.base_url = base_url.rstrip("/")  # чтобы не было двойных слэшей

    def set_auth_token(self, token: str):
        """Устанавливаем токен авторизации для всех последующих запросов."""
        self._update_session_headers(headers={"Authorization": f"Bearer {token}"})

    def send_request(
            self,
            method: str,
            endpoint: str,
            data: Dict | BaseModel | None = None,
            params: Dict | None = None,
            expected_status: Iterable[int] = (200,),
            need_logging: bool = True
    ) -> requests.Response:

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        # Если это модель pydantic, то мы ее переводим в json
        if isinstance(data, BaseModel):
            data = json.loads(data.model_dump_json(exclude_unset=True))

        request_kwargs: Dict = {
            "headers": self.headers
        }

        if params:
            request_kwargs["params"] = params

        if data and method.upper() != "GET":
            request_kwargs["json"] = data

        with allure.step(f"HTTP {method} {url}"):
            response = self.session.request(method, url, **request_kwargs)

            allure.attach(
                str(request_kwargs),
                name="REQUEST",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                str(response.status_code),
                name="STATUS",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                response.text,
                name="RESPONSE",
                attachment_type=allure.attachment_type.JSON
            )

        if need_logging:
            self.log_request_and_response(response)

        if response.status_code not in expected_status:
            raise ValueError(
                f"Unexpected status code: {response.status_code}. Expected: {expected_status}"
            )

        return response

    def log_request_and_response(self, response: requests.Response):
        """
        Логирование запросов и ответов. Настройки логирования описаны в pytest.ini
        Преобразует вывод в curl-like (-H хедеры), (-d тело)

        :param response: Объект response получаемый из метода "send_request"
        """
        try:
            request = response.request
            headers = " \\\n".join([f"-H '{header}: {value}'" for header, value in request.headers.items()])
            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            body = ""
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode('utf-8')
                elif isinstance(request.body, str):
                    body = request.body
                body = f"-d '{body}' \n" if body != '{}' else ''

            self.logger.info(
                f"{GREEN}{full_test_name}{RESET}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            response_status = response.status_code
            is_success = response.ok
            response_data = response.text
            if not is_success:
                self.logger.info(f"\tRESPONSE:"
                                 f"\nSTATUS_CODE: {RED}{response_status}{RESET}"
                                 f"\nDATA: {RED}{response_data}{RESET}")
        except Exception as e:
            self.logger.info(f"\nLogging went wrong: {type(e)} - {e}")

    def _update_session_headers(self, **kwargs: Unpack[HeadersKwargs]):
        """
        Обновление заголовков сессии.
        :param session: Объект requests. Session, предоставленный API-классом.
        :param kwargs: Дополнительные заголовки.
        """
        if "headers" in kwargs:
            self.headers.update(kwargs["headers"]) # Обновляем базовые заголовки
            self.session.headers.update(self.headers) # Обновляем заголовки в текущей сессии

