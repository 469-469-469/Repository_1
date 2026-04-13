from typing import Optional

from sqlalchemy.orm import Session
from db_requester.db_models.user import UserDBSheme
from db_requester.db_models.movie import MovieDBSheme
from models.users_base_models import RequestTestUser


class DBHelper:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    """Класс с методами для работы с БД в тестах"""

    def create_test_user(self, user_data: RequestTestUser) -> UserDBSheme:
        """Создает тестового пользователя"""
        user_data = user_data.model_dump()
        user = UserDBSheme(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_user_by_id(self, user_id: str) -> Optional[UserDBSheme]:
        """Получает пользователя по ID"""
        return self.db_session.query(UserDBSheme).filter(UserDBSheme.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[UserDBSheme]:
        """Получает пользователя по email"""
        return self.db_session.query(UserDBSheme).filter(UserDBSheme.email == email).first()

    def get_movie_by_name(self, name: str) -> Optional[MovieDBSheme]:
        """Получает фильм по названию"""
        return self.db_session.query(MovieDBSheme).filter(MovieDBSheme.name == name).first()

    def get_movie_by_id(self, movie_id: int) -> Optional[MovieDBSheme]:
        """Получает фильм по ID"""
        return self.db_session.query(MovieDBSheme).filter(MovieDBSheme.id == str(movie_id)).first()

    def user_exists_by_email(self, email: str) -> bool:
        """Проверяет существование пользователя по email"""
        return self.db_session.query(UserDBSheme).filter(UserDBSheme.email == email).count() > 0

    def delete_user(self, user: UserDBSheme):
        """Удаляет пользователя"""
        self.db_session.delete(user)
        self.db_session.commit()

    def cleanup_test_data(self, objects_to_delete: list):
        """Очищает тестовые данные"""
        for obj in objects_to_delete:
            if obj:
                self.db_session.delete(obj)
        self.db_session.commit()


'''
Пример хелпера для movies
def get_movie_by_id(self, movie_id: str):
    """Получает фильм по ID"""
    return self.db_session.query(MovieDBSheme).filter(MovieDBSheme.id == movie_id).first()
'''
