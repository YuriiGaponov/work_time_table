from aiohttp import ClientSession
from asyncio import gather, Semaphore, TimeoutError
from datetime import datetime, timedelta
from typing import AsyncGenerator, Generator, Optional, Tuple

from app.core import Config


class CalendarService:
    """Сервис для работы с календарными данными через API."""

    @classmethod
    def iterate_days_in_year(
        cls, year: int
    ) -> Generator[Tuple[int, int, int], None]:
        """
        Генерирует даты всех дней заданного года.

        Args:
            year (int): Год для генерации дат.

        Yields:
            Tuple[int, int, int]: Кортеж (год, месяц, день)
            для каждого дня года.
        """
        current_date = datetime(year, 1, 1)

        while current_date.year == year:
            yield current_date.year, current_date.month, current_date.day
            current_date += timedelta(days=1)

    @classmethod
    async def fetch_day(
        cls,
        session: ClientSession,
        y: int,
        m: int,
        d: int
    ) -> Optional[str]:
        """
        Получает данные для конкретного дня через API календаря.

        Args:
            session (ClientSession): HTTP‑сессия для выполнения запроса.
            y (int): Год.
            m (int): Месяц.
            d (int): День.

        Returns:
            Optional[str]: Текст ответа от API или None при ошибке.
        """
        url = f'{Config.CALENDAR_API_URL}{y}/{m}/{d}'
        try:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"Ошибка {response.status} при запросе {url}")
                    return None
        except TimeoutError:
            print(f"Таймаут при запросе {url}")
            return None
        except Exception as e:
            print(f"Ошибка при запросе {url}: {e}")
            return None

    @classmethod
    async def fetch_with_semaphore(
        cls,
        y: int,
        m: int,
        d: int,
        session: ClientSession,
        max_concurrent: int
    ) -> Optional[str]:
        """
        Выполняет запрос к API с ограничением параллельных запросов.

        Args:
            y (int): Год.
            m (int): Месяц.
            d (int): День.
            session (ClientSession): HTTP‑сессия.
            max_concurrent (int): Максимальное число параллельных запросов.

        Returns:
            Optional[str]: Результат выполнения fetch_day.
        """
        async with Semaphore(max_concurrent):
            return await cls.fetch_day(session, y, m, d)

    @classmethod
    async def get_days(
        cls,
        year: int,
        session: ClientSession,
        max_concurrent: int = 50
    ) -> AsyncGenerator[str, None]:
        """
        Асинхронно получает данные календаря для всех дней года.

        Использует семафор для ограничения числа параллельных запросов.

        Args:
            year (int): Год для получения данных.
            session (ClientSession): HTTP‑сессия.
            max_concurrent (int): Макс. число параллельных запросов.

        Yields:
            str: Данные дня от API (если запрос успешен).
        """
        # Создаём задачи для всех дней
        tasks = [
            cls.fetch_with_semaphore(y, m, d, session, max_concurrent)
            for y, m, d in cls.iterate_days_in_year(year)
        ]

        # Выполняем все задачи параллельно и собираем результаты
        results = await gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                print(f"Неожиданная ошибка: {result}")
            elif result is not None:
                yield result

    @classmethod
    async def get_calendar(cls, year: int) -> None:
        """
        Получает и выводит календарные данные за указанный год.

        Создаёт HTTP‑сессию и асинхронно запрашивает данные по всем дням года.

        Args:
            year (int): Год для получения календаря.
        """
        async with ClientSession() as session:
            async for day in cls.get_days(year, session):
                print(day)
