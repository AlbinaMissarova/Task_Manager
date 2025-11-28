# Настройки базы данных и подключение к ней
import os
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

# Создаем директорию для данных если ее нет
os.makedirs('./data', exist_ok=True)

database_url = 'sqlite+aiosqlite:///./data/db.sqlite3'
async_engine = create_async_engine(url=database_url)
async_session_factory = async_sessionmaker(async_engine, class_=AsyncSession)

# Базовый класс для всех ORM моделей
class Base(DeclarativeBase):
    pass
