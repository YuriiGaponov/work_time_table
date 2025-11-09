"""Тесты для сервиса календаря.

Модуль содержит тестовые сценарии для проверки работоспособности
календарного API, включая:
- доступность основного эндпоинта;
- корректность возвращаемых HTTP‑статусов.

Используемые зависимости:
- requests: для выполнения HTTP‑запросов;
- http.HTTPStatus: для проверки кодов состояния;
- app.core.Config: для получения URL API из конфигурации.
"""

import requests
from http import HTTPStatus

from app.core import Config


class TestCalendarService:
    """Тестовый класс для проверки сервиса календаря."""

    @classmethod
    def test_calendar_api_available(cls):
        """Проверяет доступность главного эндпоинта календарного API."""
        response = requests.get(Config.CALENDAR_API_URL)
        assert response.status_code == HTTPStatus.OK
