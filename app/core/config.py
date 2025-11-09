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
        BASE_DIR: корневая директория проекта
        SECRET_KEY: секретный ключ приложения
        DEBUG: флаг режима отладки
        TEMPLATES_FOLDER: путь к директории с шаблонами
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

    DATABASE_URL: str = os.getenv('DATABASE_URL')
    """
    URL подключения к базе данных

    Важно:
    - значение должно быть задано в переменных окружения в среде выполнения;
    - запрещено хранить значение в коде приложения из соображений безопасности;
    """

    SQLALCHEMY_DATABASE_URI: str = os.getenv('SQLALCHEMY_DATABASE_URI')
    """
    URI подключения к базе данных для SQLAlchemy.

    Особенности:
    - Является альтернативным источником конфигурации по отношению
    к DATABASE_URL.
        В данном приложении в значение передаются данные
     для создания синхронного движка БД.
    """

    CALENDAR_API_URL: str = 'https://calendar.kuzyak.in/api/calendar/'
