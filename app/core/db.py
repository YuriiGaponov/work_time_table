"""
Модуль для настройки асинхронного взаимодействия с базой данных.

Содержит:
- асинхронный движок SQLAlchemy (async_engine);
- фабрику асинхронных сессий (AsyncSessionLocal);
- базовый класс для моделей (PreBase) с предустановленными параметрами;
- базовый декларативный класс ORM (Base);
- функцию создания таблиц в БД (create_tables).

Использует конфигурацию из .config.Config для подключения к БД.
Предоставляет готовую инфраструктуру для определения и работы
с моделями SQLAlchemy в асинхронном приложении.
"""

from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declared_attr, declarative_base, sessionmaker

from .config import Config

# Создаёт асинхронный движок для работы с базой данных
# на основе URL из конфигурации.
async_engine = create_async_engine(Config.DATABASE_URL)

# Фабрика асинхронных сессий для взаимодействия с БД.
# Использует созданный асинхронный движок и класс AsyncSession.
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession
)


class PreBase():
    """
    Базовый класс с предустановленными параметрами для моделей БД.

    Обеспечивает автоматическое формирование имени таблицы
    на основе имени класса и добавляет поле id.
    """

    @declared_attr
    def __tablename__(cls):
        """Формирует имя таблицы как строчное имя класса."""
        return cls.__name__.lower()

    # Первичный ключ для всех моделей, наследующих PreBase.
    id = Column(Integer, primary_key=True)


# Базовый класс для всех моделей ORM.
# Наследует предустановленные параметры из PreBase.
Base = declarative_base(cls=PreBase)


async def create_tables():
    """
    Создаёт все таблицы в базе данных согласно определениям моделей.

    Использует метаданные Base для генерации SQL-запросов создания таблиц.
    Операция выполняется в асинхронном контексте.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
