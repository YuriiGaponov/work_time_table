"""
Набор тестовых сценариев для проверки работоспособности подключения
к базе данных через SQLAlchemy (как в асинхронном, так и в синхронном режимах).

Функционал:
- test_db_async_connection: проверяет асинхронное подключение к БД,
  выполняя простой SQL‑запрос `SELECT 1` и валидируя результат.
- test_db_connection: аналогично мпроверяет синхронное подключение к БД.
"""

import pytest
from sqlalchemy import text


class TestDBConnection:
    """Тесты подключения к БД (асинхронное и синхронное)."""

    @classmethod
    @pytest.mark.asyncio
    async def test_db_async_connection(cls):
        """
        Проверяет асинхронное подключение:
        выполняет SELECT 1 и проверяет результат.
        """
        from app.core.db import async_engine

        async with async_engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            row = result.fetchone()

        assert row is not None
        assert row[0] == 1

    @classmethod
    def test_db_connection(cls):
        """
        Проверяет синхронное подключение:
        выполняет SELECT 1 и проверяет результат.
        """
        from app.core.db import engine

        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            row = result.fetchone()

        assert row is not None
        assert row[0] == 1
