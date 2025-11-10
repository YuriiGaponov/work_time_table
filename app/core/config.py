"""Модуль конфигурации приложения.

Загружает параметры из переменных окружения для безопасности
и гибкости настройки.
"""

import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()


class Config:
    """Базовый класс для хранения конфигурационных параметров приложения.
    Параметры загружаются из переменных окружения.

    Атрибуты:
        BASE_DIR: корневая директория проекта (вычисляется автоматически);
        SECRET_KEY: секретный ключ для криптографических операций;
        DEBUG: флаг режима отладки (True/False);
        TEMPLATES_FOLDER: путь к директории с шаблонами;
        YEARS: список допустимых годов для работы с календарями;
        DATA_DIR: путь к директории для хранения данных приложения;
        DB_PATH: полный путь к файлу базы данных;
        DATABASE_URL: URL для подключения к БД (общий формат);
        SQLALCHEMY_DATABASE_URI: URI для SQLAlchemy (синхронный движок);
        CALENDAR_API_URL: базовый URL API календаря.
    """

    BASE_DIR = Path(__file__).parent.parent.parent
    """Корневая директория проекта для построения путей."""

    SECRET_KEY: str = os.getenv('SECRET_KEY')
    """Секретный ключ для подписи токенов, защиты сессий и криптографии."""

    DEBUG: bool = os.getenv('DEBUG', default=False) == 'True'
    """Режим отладки: True — разработка, False — рабочий режим."""

    TEMPLATES_FOLDER: str = BASE_DIR / (
        os.getenv('TEMPLATES_FOLDER') or 'templates'
    )
    """
    Путь к шаблонам: BASE_DIR + значение TEMPLATES_FOLDER
    (по умолчанию 'templates').
    """

    YEARS = list(
        range(
            int(os.getenv('MIN_YEAR')), int(os.getenv('MAX_YEAR')) + 1
        )
    )
    """
    Список допустимых годов (целых чисел),
    с календарями которых работает приложение.
    """

    DATA_DIR = os.path.join(BASE_DIR, os.getenv('DATA_DIR'))
    """
    Путь к директории данных. Формируется из BASE_DIR и переменной DATA_DIR.
    """

    DB_PATH = os.path.join(DATA_DIR, os.getenv('DB_NAME'))
    """
    Полный путь к файлу БД. Собирается из DATA_DIR и переменной DB_NAME.
    """

    DATABASE_URL: str = f'{os.getenv('DATABASE_URL')}{DB_PATH}'
    """
    URL для подключения к БД. Комбинация переменной DATABASE_URL и DB_PATH.
    """

    SQLALCHEMY_DATABASE_URI: str = (
        f'{os.getenv('SQLALCHEMY_DATABASE_URI')}{DB_PATH}'
    )
    """
    URI для SQLAlchemy. Формируется из переменной
    SQLALCHEMY_DATABASE_URI и DB_PATH.
    Используется для синхронного движка БД.
    """

    CALENDAR_API_URL: str = 'https://calendar.kuzyak.in/api/calendar/'
    """
    Базовый URL API календаря. Фиксированное значение
    (не требует настройки через окружение).
    Используется для формирования запросов к сервису.
    """
