from typing import Optional
from pydantic import EmailStr
from pydantic import BaseModel, Field, model_validator
from enum import Enum
from venv import logger


class Roles(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPERADMIN = "SUPERADMIN"


class RequestTestUser(BaseModel):
    email: EmailStr
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


def pydantic_user_request(creation_user_data: dict) -> RequestTestUser:
    pydantic_user = RequestTestUser(**creation_user_data)
    log_json = pydantic_user.model_dump_json()
    logger.info(f"Логируем Pydantic {log_json}")
    return pydantic_user


class ResponseTestUser(BaseModel):
    id: Optional[str] = None
    email: EmailStr
    fullName: str
    password: Optional[str] = None
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None


    @model_validator(mode="after")
    def check_user_match(self):
        if "@" not in self.email:
            raise ValueError("В эмейл нет символа '@'")
        return self


def pydantic_user_response(response_user: dict) -> ResponseTestUser:
    pydantic_user = ResponseTestUser(**response_user)
    log_json = pydantic_user.model_dump_json()
    logger.info(f"Логируем Pydantic {log_json}")

    return pydantic_user

