import allure
from pydantic import EmailStr
from pydantic import BaseModel,  model_validator
from venv import logger


class CredsModel(BaseModel):
    email: EmailStr
    password: str

    @model_validator(mode="after")
    def check_user_match(self):
        if "@" not in self.email:
            raise ValueError("В эмейл нет символа '@'")
        if len(self.password) < 8:
            raise ValueError("Пароль меньше 8 символов")
        return self


@allure.step("Валидация данных кредов")
def pydantic_user_creds(creds: dict) -> CredsModel:
    pydantic_creds = CredsModel(**creds)
    log_json = pydantic_creds.model_dump_json()
    logger.info(f"Логируем Pydantic {log_json}")

    return pydantic_creds