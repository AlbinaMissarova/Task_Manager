# Данный файл содержит описание всех сущностей базы данных

from typing import Annotated
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base

# intpk - integer primary key - вводим новый тип данных
intpk = Annotated[int, mapped_column(primary_key=True)]

# товары
class  TaskOrm(Base):
    __tablename__ = "tasks"

    # Номер задачи
    task_id: Mapped[intpk]
    # Название задачи
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)  
    # Описание задачи
    description: Mapped[str] = mapped_column(String, nullable=True)  
    # Статус (выполнены/не выполнено)
    completed: Mapped[Boolean] = mapped_column(Boolean, nullable=False)  