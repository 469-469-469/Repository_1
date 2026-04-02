import random
import string
from faker import Faker
faker = Faker()


class DataGenerator:
    
    @staticmethod
    def generate_random_email():
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_name():
        return f"{faker.first_name()} {faker.last_name()}"
         
    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 буква с большой буквой.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """

        upper = random.choice(string.ascii_uppercase)
        lower = random.choice(string.ascii_lowercase)
        digit = random.choice(string.digits)
        special = random.choice("!@#$%^&*")

        other = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        # Перемешиваем пароль для рандомизации
        password = list(upper + lower + digit + special + other)
        random.shuffle(password)

        return ''.join(password)