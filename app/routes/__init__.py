"""
Пакет маршрутов веб‑приложения.

Содержит endpoints для обработки HTTP‑запросов.

Импортирует:
- `calendar` из `.calendar`;
- `main` из `.index`.

Экспортирует через `__all__`: `calendar`, `main`.

Для добавления нового маршрута:
1. Создайте/обновите модуль с маршрутом.
2. Добавьте имя в `__all__`.
"""

from .calendar import calendar
from .index import main

__all__ = ['calendar', 'main']
