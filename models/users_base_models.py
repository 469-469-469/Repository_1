from typing import Optional
from pydantic import EmailStr
from pydantic import BaseModel, Field, model_validator
from enum import Enum
from venv import logger
import pytest_check as check

class Roles(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPERADMIN = "SUPERADMIN"


class RequestTestUser(BaseModel):
    email: str = EmailStr
    fullName: str
    password: str
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="Пароли должны совпадать")
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @model_validator(mode="after")
    def check_user_match(self):
        if self.password != self.passwordRepeat:
            raise ValueError("Пароли не совпадают")
        if "@" not in self.email:
            raise ValueError("В эмейл нет символа '@'")
        if len(self.password) < 8:
            raise ValueError("Пароль меньше 8 символов")
        return self


def pydantic_user_request(test_user: dict):
    pydantic_user = RequestTestUser(**test_user)
    log_json = pydantic_user.model_dump_json()
    logger.info(f"Логируем Pydantic {log_json}")  # а также возможность удобного взаимодействия
    return pydantic_user.model_dump()  # <- возвращаем словарь


class ResponseTestUser(BaseModel):
    email: str = EmailStr
    fullName: str
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @model_validator(mode="after")
    def check_user_match(self):
        if "@" not in self.email:
            raise ValueError("В эмейл нет символа '@'")
        return self

# Проверки данных пользователя из ответа от сервера,  + при получении request_user сравнивается с ним
def pydantic_user_response(response_user: dict, request_user: dict=None):
    pydantic_user = ResponseTestUser(**response_user)
    log_json = pydantic_user.model_dump_json()
    logger.info(f"Логируем Pydantic {log_json}")  # а также возможность удобного взаимодействия

    pydantic_user = pydantic_user.model_dump() # <- превращаем в словарь
    if request_user:
        fields_to_check = ["email", "fullName", "roles"]

        for field in fields_to_check:
            check.equal(
                pydantic_user.get(field),
                request_user.get(field),
                f"{field} не совпадает с отправленным"
            )

        check.is_true(
            pydantic_user.get("verified"),
            "verified должен быть True"
        )

    return pydantic_user
