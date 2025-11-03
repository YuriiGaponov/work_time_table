"""Маршрут /calendar для отображения календарного интерфейса."""

from flask import render_template
from .. import app


@app.route('/calendar')
def calendar():
    """Обработчик GET‑запроса для маршрута /calendar.

    Получает список лет из конфигурации приложения (app.config['YEARS'])
    и рендерит шаблон календарного интерфейса.

    Returns:
        str: HTML‑код страницы календаря, сгенерированный на основе шаблона
        'calendar/get_calendar.html' с переданным параметром years.
    """
    years = app.config['YEARS']

    return render_template('calendar/get_calendar.html', years=years)
