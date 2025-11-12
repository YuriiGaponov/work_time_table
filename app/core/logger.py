"""
Модуль предоставляет инструменты для централизованной настройки логирования.
Он отвечает за создание и конфигурацию логгера, который будет использоваться
во всем приложении для записи информации, предупреждений и ошибок.

Основные возможности:
* Автоматическая конфигурация уровня логирования
* Ротация лог-файлов
* Форматирование сообщений лога
* Интеграция с Flask-приложением

Структура модуля:
* Класс Logger - основной класс для настройки логирования
* Константы конфигурации
* Методы для работы с уровнями логирования
"""

import logging
import os
from dotenv import load_dotenv
from flask import Flask
from logging.handlers import RotatingFileHandler

from .config import Config

load_dotenv()


class Logger:
    """
    Класс для настройки и конфигурации логирования в приложении.

    Предоставляет методы для настройки уровня логирования,
    конфигурации обработчика файлов логов и других параметров.
    """

    LOG_DIR = Config.BASE_DIR / os.getenv('LOG_DIR')
    """
    Путь к директории для хранения логов приложения.
    Формируется на основе BASE_DIR из конфигурации и значения из .env файла.
    """

    LOG_FILE_NAME: str = 'app.log'
    """
    Имя файла, в который будут записываться логи приложения.
    Включает расширение .log для корректного распознавания типа файла.
    """

    LOG_MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', '1000000'))
    """
    Максимальный размер одного лог‑файла в байтах.
    Когда файл достигает указанного размера, создается новый файл.
    """

    LOG_BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', '0'))
    """
    Количество резервных копий лог‑файлов, сохраняемых при ротации.
    После превышения этого числа самые старые файлы удаляются.
    """

    LOG_ENCODING: str = os.getenv('LOG_ENCODING')
    """
    Кодировка, используемая для записи логов в файл.
    Берется из переменной окружения LOG_ENCODING.
    """

    HANDLER_MODE = 'a'
    """
    Режим открытия файла для записи логов.
    'a' - режим добавления (append), новые записи добавляются в конец файла.
    """

    @classmethod
    def logging_level(cls) -> int:
        """
        Определяет уровень логирования в зависимости от окружения.

        Возвращает уровень DEBUG, если переменная окружения DEBUG установлена,
        иначе возвращает уровень INFO.

        Returns:
            int: Уровень логирования (DEBUG или INFO)
        """
        return logging.DEBUG if os.getenv('DEBUG') else logging.INFO

    @classmethod
    def configure_logger(cls, app: Flask) -> None:
        """
        Настраивает логирование для Flask-приложения.

        Создает RotatingFileHandler для записи логов в файл,
        настраивает форматтер и добавляет обработчик к логгеру приложения.

        Args:
            app (Flask): Экземпляр Flask-приложения

        Raises:
            FileNotFoundError: Если директория для логов не существует
            IOError: Если возникли проблемы с созданием файла логов
        """
        handler = RotatingFileHandler(
            f'{cls.LOG_DIR}/{cls.LOG_FILE_NAME}',
            mode=cls.HANDLER_MODE,
            maxBytes=cls.LOG_MAX_BYTES,
            backupCount=cls.LOG_BACKUP_COUNT,
            encoding=cls.LOG_ENCODING
        )
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        app.logger.addHandler(handler)
        app.logger.setLevel(Logger.logging_level())
