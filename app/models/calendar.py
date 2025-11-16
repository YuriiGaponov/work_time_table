"""
Модели для хранения данных о днях года календаря.

Зависимости: sqlalchemy, app.core.Base.
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime
)

from app.core import Base
from .schemas import CalendarDayInfo


class CalendarDay(Base):
    """
    Календарный день в системе.

    Атрибуты:
        year (int): год (обязательный).
        month_name (str): название месяца (до 20 симв., обязательный).
        date (datetime): дата (обязательный).
        is_working_day (bool): рабочий день (по умолч. True).
        is_short_day (bool): сокращённый день (по умолч. False).
        holiday (str|None): название праздника (до 100 симв.).
    """

    year = Column(Integer, nullable=False)
    month_name = Column(String(20), nullable=False)
    date = Column(DateTime, nullable=False, unique=True)
    is_working_day = Column(Boolean, nullable=False, default=True)
    is_short_day = Column(Boolean, nullable=False, default=False)
    holiday = Column(String(100), nullable=True)

    def __repr__(self):
        return f'{self.date}{', 'f'{self.holiday}' if self.holiday else ''}'


class CalendarDayService:
    """
    Сервис для работы с календарными днями.

    Содержит методы для:
    - преобразования строкового представления даты в объект datetime;
    - создания экземпляра CalendarDay на основе данных из API.
    """

    @classmethod
    def extract_date(cls, date_string: str) -> datetime:
        """Преобразует строку с датой в объект datetime.date."""
        dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        return dt.date()

    @classmethod
    def get_calendar_day_from_api(
        cls, api_data: CalendarDayInfo
    ) -> CalendarDay:
        """
        Создаёт экземпляр CalendarDay на основе данных, полученных из API.
        """
        return CalendarDay(
            year=int(api_data['year']),
            month_name=api_data['month']['name'],
            date=cls.extract_date(api_data['date']),
            is_working_day=api_data['isWorkingDay'] == 'True',
            is_short_day=api_data['isShortDay'] == 'True',
            holiday=api_data.get('holiday', None)
        )
