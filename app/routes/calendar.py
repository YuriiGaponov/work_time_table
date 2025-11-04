"""Маршрут /calendar для отображения календарного интерфейса."""

from flask import request, render_template
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


@app.route('/download-calendar', methods=['POST'])
def download_calendar():
    selected_year = request.form.get('year', type=int)
    app.logger.info(
        f'На эндпоинт /download-calendar передано значение года'
        f' для скачивания календаря: {selected_year}'
    )

    if not selected_year or selected_year not in app.config['YEARS']:
        return "Некорректный год", 400

    return f"Календарь за {selected_year} год успешно загружен!"
