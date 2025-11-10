"""
Модели для хранения данных о днях года календаря.

Зависимости: sqlalchemy, app.core.Base.
"""

from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime
)

from app.core import Base


class CalendarDay(Base):
    """
    Календарный день в системе.

    Атрибуты:
        year (int): год (обязательный).
        month_name (str): название месяца (до 20 симв., обязательный).
        date (datetime): дата (обязательный).
        is_working_day (bool): рабочий день (по умолч. True).
        is_short_day (bool): сокращённый день (по умолч. False).
        status_code (int): код статуса (обязательный).
        holiday (str|None): название праздника (до 100 симв.).
    """

    year = Column(Integer, nullable=False)
    month_name = Column(String(20), nullable=False)
    date = Column(DateTime, nullable=False)
    is_working_day = Column(Boolean, nullable=False, default=True)
    is_short_day = Column(Boolean, nullable=False, default=False)
    holiday = Column(String(100), nullable=True)
