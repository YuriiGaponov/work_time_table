"""Маршрут /calendar для отображения календарного интерфейса."""

from flask import render_template
from .. import app


@app.route('/calendar')
def calendar():
    """Обработчик GET‑запроса для /calendar.

    Рендерит и возвращает шаблон календаря.

    Returns:
        str: HTML‑код страницы календаря.
    """
    return render_template('calendar/get_calendar.html')
