# Данный файл содержит реализацию всех необходимых запросов в БД
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from src.database import Base, async_engine, async_session_factory
from src.models import TaskOrm
from src.schemas import TaskAddDTO, TaskDTO, TaskUpdateDTO

# взаимодействие с БД в асинхронном режиме
class AsyncORM:
    # создание всех таблиц
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # ===================== CREATE - ФУНКЦИЯ ДОБАВЛЕНИЯ =====================
    @classmethod
    async def insert_task(cls, data: TaskAddDTO) -> TaskDTO:
        async with async_session_factory() as session:
            try:
                task_dict = data.model_dump()
                task = TaskOrm(**task_dict)
                session.add(task)
                await session.commit()
                # для получения присвоенного ID
                await session.refresh(task) 
                task_dto = TaskDTO.model_validate(task)
                return task_dto
            except IntegrityError as e:
                await session.rollback()
                
                # Анализируем текст ошибки для определения конкретного нарушения
                error_msg = str(e.orig).lower()
                
                if "title" in error_msg and "unique" in error_msg:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Задача с таким названием уже существует."
                    )

    # ===================== READ - SELECT ЗАПРОСЫ - ПОЛУЧЕНИЕ ИНФОРМАЦИИ =====================
    # Получение всех задач
    @classmethod
    async def get_all_tasks(cls) -> list[TaskDTO]:
        async with async_session_factory() as session:        
            query = (
                select(TaskOrm)
                # сортировка в порядке возрастания ID
                .order_by(TaskOrm.task_id.asc())
            )
            res = await session.execute(query)
            result_orm = res.unique().scalars().all() 
            result_dto = [TaskDTO.model_validate(row, from_attributes=True) for row in result_orm]
            return result_dto
        
    # Получение одной задачи по ID
    @classmethod
    async def get_task_by_ID(cls, task_id : int) -> TaskDTO:
        async with async_session_factory() as session:
            task = await session.get(TaskOrm, task_id)
            if task:
                task_dto = TaskDTO.model_validate(task)
                return task_dto
            else: 
                raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Задачи с таким ID нет."
                    )
    # ===================== UPDATE - ИЗМЕНЕНИЕ ЗАПИСЕЙ В БД =====================
    @classmethod
    async def update_task(cls, task_id : int, new_data:TaskUpdateDTO) -> TaskDTO:
        async with async_session_factory() as session:
            task = await session.get(TaskOrm, task_id)
            if task:
                if new_data.title is None:
                    new_data.title = task.title
                if new_data.description is None:
                    new_data.description = task.description
                if new_data.completed is None:
                    new_data.completed = task.completed

                stmt = (
                    update(TaskOrm)
                    .where(TaskOrm.task_id == task_id)
                    .values(title=new_data.title, description = new_data.description, completed=new_data.completed)
                )
                await session.execute(stmt)
                await session.commit()
                res = await session.get(TaskOrm, task_id)
                result_dto = TaskDTO.model_validate(res)
                return result_dto
            else: 
                raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Задачи с таким ID нет."
                    )

    # ===================== DELETE - УДАЛЕНИЕ =====================
    @classmethod
    async def delete_task(cls, task_id: int):
        async with async_session_factory() as session:
            task = await session.get(TaskOrm, task_id)
            if task:
                await session.delete(task)
                await session.commit()  
            else: 
                raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Задачи с таким ID нет."
                    )