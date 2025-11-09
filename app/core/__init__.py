"""
Основной пакет приложения, содержащий базовую инфраструктуру и конфигурацию.

Этот пакет является центральным компонентом приложения и включает в себя:
* Инициализацию Flask-приложения
* Базовую конфигурацию
* Основные служебные функции

Структура пакета:
* app.py - фабрика создания Flask-приложения
* config.py - конфигурационные настройки
* db.py - настройки и подключение к базе данных
* logger.py - система логирования
"""

from .app import create_app
from .config import Config
from .db import AsyncSessionLocal, Base, create_tables, SessionLocal

__all__ = [
    'AsyncSessionLocal',
    'Base',
    'Config',
    'create_app',
    'create_tables',
    'SessionLocal'
]
