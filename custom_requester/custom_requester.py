import json
import logging
import os
from typing import Dict, Iterable
from typing_extensions import Unpack

import requests
from typing_extensions import TypedDict


class HeadersKwargs(TypedDict, total=False):
    headers: Dict[str, str]


class CustomRequester:

    """Кастомный реквестер для стандартизации и упрощения отправки HTTP-запросов."""

    base_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    def __init__(self, session: requests.Session, timeout: float = 10):
        self.session = session
        self.timeout = timeout
        self.headers = self.base_headers.copy()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def send_request(
            self,
            method: str,
            base_url: str,
            endpoint: str,
            data: Dict | None = None,
            params: Dict | None = None,
            expected_status: Iterable[int] = (200,),
            need_logging: bool = True
    ) -> requests.Response:

        url = f"{base_url}{endpoint}"

        request_kwargs: Dict = {
            "headers": self.headers
        }

        if params:
            request_kwargs["params"] = params

        if data and method.upper() != "GET":
            request_kwargs["json"] = data

        response = self.session.request(method, url, **request_kwargs)

        if need_logging:
            self.log_request_and_response(response)

        if response.status_code not in expected_status:
            raise ValueError(
                f"Unexpected status code: {response.status_code}. Expected: {expected_status}"
            )

        return response


    def log_request_and_response(self, response: requests.Response):
        try:
            request = response.request
            green = '\033[32m'
            red = '\033[31m'
            reset = '\033[0m'
            headers = " \\\n".join([f"-H '{header}: {value}'" for header, value in request.headers.items()])
            full_test_name = f"pytest {os.environ.get('PYTEST_CURRENT_TEST', '').replace(' (call)', '')}"

            body = ""
            if hasattr(request, 'body') and request.body is not None:
                if isinstance(request.body, bytes):
                    body = request.body.decode('utf-8')
                body = f"-d '{body}' \n" if body != '{}' else ''

            self.logger.info(f"\n{'=' * 40} REQUEST {'=' * 40}")
            self.logger.info(
                f"{green}{full_test_name}{reset}\n"
                f"curl -X {request.method} '{request.url}' \\\n"
                f"{headers} \\\n"
                f"{body}"
            )

            response_data = response.text
            try:
                response_data = json.dumps(json.loads(response.text), indent=4, ensure_ascii=False)
            except json.JSONDecodeError:
                pass

            self.logger.info(f"\n{'=' * 40} RESPONSE {'=' * 40}")
            if not response.ok:
                self.logger.info(
                    f"\tSTATUS_CODE: {red}{response.status_code}{reset}\n"
                    f"\tDATA: {red}{response_data}{reset}"
                )
            else:
                self.logger.info(
                    f"\tSTATUS_CODE: {green}{response.status_code}{reset}\n"
                    f"\tDATA:\n{response_data}"
                )
            self.logger.info(f"{'=' * 80}\n")
        except Exception as e:
            self.logger.error(f"\nLogging failed: {type(e)} - {e}")

    def _update_session_headers(self, **kwargs: Unpack[HeadersKwargs]):
        """
        Обновление заголовков сессии.
        :param session: Объект requests. Session, предоставленный API-классом.
        :param kwargs: Дополнительные заголовки.
        """
        if "headers" in kwargs:
            self.headers.update(kwargs["headers"]) # Обновляем базовые заголовки
            self.session.headers.update(self.headers) # Обновляем заголовки в текущей сессии

