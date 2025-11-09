import aiohttp
from datetime import datetime, timedelta

from app.core import Config


def iterate_days_in_year(year):
    # Начинаем с 1 января заданного года
    current_date = datetime(year, 1, 1)

    # Пока год не изменился — продолжаем цикл
    while current_date.year == year:
        yield current_date.year, current_date.month, current_date.day
        current_date += timedelta(days=1)


async def get_calendar(year):
    """
    Асинхронно получает данные календаря для всех дней заданного года.

    Args:
        year (int): Год, для которого нужно получить календарь.
    """
    # Создаем сессию aiohttp
    # (лучше передавать извне для повторного использования)
    async with aiohttp.ClientSession() as session:
        # Перебираем все дни года
        for y, m, d in iterate_days_in_year(year):
            url = f'{Config.CALENDAR_API_URL}{y}/{m}/{d}'
            try:
                async with session.get(url) as response:
                    # Ждем ответа и читаем текст
                    text = await response.text()
                    print(text)
            except Exception as e:
                print(f"Ошибка при запросе {url}: {e}")
