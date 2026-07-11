# Coursework: Aircraft Monitoring System

Система для мониторинга самолетов в воздушном пространстве стран через API.

## Функциональность

- Получение географических координат стран через Nominatim API
- Получение информации о самолетах через OpenSky Network API
- Сохранение данных в JSON файл
- Фильтрация и сортировка самолетов по различным критериям
- Интерактивное взаимодействие с пользователем через консоль

## Установка и запуск

```bash
# Клонирование репозитория
git clone <repository-url>
cd coursework

# Установка зависимостей
poetry install --no-root

# Запуск программы
poetry run python main.py

# Запуск тестов
poetry run pytest -v

# Запуск тестов с покрытием
poetry run pytest --cov=src --cov-report=term

# Структура проекта

coursework_2/
├── src/
│   ├── __init__.py          # Инициализация
│   ├── abstract_api.py      # Абстрактный класс для API
│   ├── aeroplanes_api.py    # Реализация API
│   ├── aeroplane.py         # Класс самолета
│   ├── abstract_storage.py  # Абстрактный класс для хранения
│   ├── json_storage.py      # Хранение в JSON
│   └── utils.py             # Утилиты
├── tests/
│   ├── __init__.py        # Инициализация
│   ├── test_aeroplane.py  # Тесты для класса самолета
│   ├── test_api.py        # Тесты для API
│   ├── test_storage.py    # Тесты для хранения
│   └── test_utils.py     # Тесты для утилит
├── data/
│   ├── aeroplanes.json      # Файл для хранения данных
│   └── test_aeroplanes.json # Тестовые данные
├── main.py        # Основной файл программы
├── poetry.lock    # Зависимости 
├── pyproject.toml # Конфигурация для Poetry
└── README.md      # Описание и инфорамация по проекту

# Технологии
Python 3.9+

requests для работы с API

pytest для тестирования

JSON для хранения данных
```

## Автор:
Геннадий Кокаулин.

## Лицензия:
Учебный проект SkyPro.



## Запуск и тестирование

```bash
# Установка зависимостей
poetry install --no-root

# Запуск программы
poetry run python main.py

# Запуск тестов
poetry run pytest -v

# Проверка покрытия
poetry run pytest --cov=src --cov-report=term
```