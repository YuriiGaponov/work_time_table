"""
Модуль для тестирования HTTP‑маршрутов веб‑приложения.
Проверяет доступность эндпоинтов и корректность HTTP‑статусов.
Использует pytest‑фикстуры и http.HTTPStatus.
"""

from http import HTTPStatus


class TestRoutes:
    """Тестовые кейсы для проверки HTTP‑маршрутов приложения."""

    @classmethod
    def test_index_page(cls, client):
        """Проверяет главную страницу (/). Ожидаемый статус: 200."""
        response = client.get('/')
        assert response.status_code == HTTPStatus.OK

    @classmethod
    def test_404_page(cls, client):
        """
        Проверяет обработку несуществующего маршрута (/nonexistent).
        Ожидаемый статус: 404.
        """
        response = client.get('/nonexistent')
        assert response.status_code == HTTPStatus.NOT_FOUND

    @classmethod
    def test_calendar_page(cls, client):
        """Проверяет страницу календаря (/calendar). Ожидаемый статус: 200."""
        response = client.get('/calendar')
        assert response.status_code == HTTPStatus.OK
