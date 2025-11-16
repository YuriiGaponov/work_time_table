from typing import TypedDict


class Month(TypedDict):
    """Типовый словарь для представления месяца."""
    name: str
    id: int


class CalendarDayInfo(TypedDict):
    """
    Типовый словарь для передачи информации о календарном дне через API.

    Атрибуты:
        year (int): год (например, 2025).
        month (Month): словарь с информацией о месяце.
        date (str): дата в формате ISO 8601 (например, "2025-01-15T00:00:00Z").
        isWorkingDay (bool): признак рабочего дня.
        isShortDay (bool): признак сокращённого рабочего дня.
        status (int): статус выходного или праздничного дня.
        holiday (str | None): название праздника при наличии.
    """
    year: int
    month: Month
    date: str  # ISO 8601
    isWorkingDay: bool
    isShortDay: bool
    status: int
    holiday: str | None
