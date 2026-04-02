# Cinescope API

Проект **Cinescope API** — набор скриптов для тестирования и работы с API. Содержит тесты и вспомогательные константы.

## Структура проекта

- `conftest.py` — конфигурация для тестов (pytest).  
- `constants.py` — константы проекта.  
- `test_API.py` — примеры тестов API.  
- `requirements.txt` — зависимости проекта.  
- `.gitignore` — файлы и папки, которые не нужно добавлять в Git.  

## Установка

1. Клонируем репозиторий:
```bash
git clone https://github.com/Honger469/Cinescope.git
cd Cinescope
Создаем виртуальное окружение:
python -m venv .venv
Активируем виртуальное окружение:
Windows:
.venv\Scripts\activate
Mac/Linux:
source .venv/bin/activate
Устанавливаем зависимости:
pip install -r requirements.txt
Запуск тестов

Запуск тестов через pytest:

pytest

Или запуск конкретного скрипта:

python test_API.py