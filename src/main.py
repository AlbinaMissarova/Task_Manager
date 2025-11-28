
from contextlib import asynccontextmanager
from typing import Annotated
from fastapi import Depends, FastAPI, status, HTTPException
from src.crud import AsyncORM
from src.schemas import TaskAddDTO, TaskDTO, TaskUpdateDTO

@asynccontextmanager
async def lifespan(app: FastAPI):
    # При запуске в первй раз будут созданы все таблицы, 
    # в остальные разы эта строчка не будет иметь никакого эффекта так как таблицы уже будут созданы
    print("Запуск приложения...")
    await AsyncORM.create_tables()
    yield
    # Shutdown code
    print("Выключение приложения...")

app = FastAPI(
    title="Task Manager API",
    description="Простой API для управления задачами для учебного занятия",
    version="1.0.0",
    lifespan=lifespan
)

@app.get(
        "/api/tasks/", 
        response_model=list[TaskDTO], 
        summary="Посмотреть список всех задач",
        tags=["Tasks"]
        )
async def get_all_tasks():
    task_list  = await AsyncORM.get_all_tasks()
    return task_list


@app.get(
        "/api/tasks/{task_id}", 
        response_model=TaskDTO, 
        summary="Посмотреть задачу по ее ID",
        tags=["Tasks"]
        )
async def get_task_by_id(task_id : int):
    try:
        task = await AsyncORM.get_task_by_ID(task_id)
        return task 
    except HTTPException:
        raise
    

@app.post(
        "/api/tasks/", 
        response_model=TaskDTO, 
        status_code=status.HTTP_201_CREATED, 
        summary="Создать новую задачу.",
        tags=["Tasks"]
        )
async def create_task(task : Annotated[TaskAddDTO, Depends()]):
    try:
        task = await AsyncORM.insert_task(task)
        return task 
    except HTTPException:
        raise
   

@app.put(
        "/api/tasks/", 
        response_model=TaskDTO, 
        summary="Изменить задачу по ее ID.",
        tags=["Tasks"]
        )
async def update_task(task_id : int, task_data : Annotated[TaskUpdateDTO, Depends()]):
    try:
        task = await AsyncORM.update_task(task_id, task_data)
        return task 
    except HTTPException:
        raise


@app.delete(
        "/api/tasks/{task_id}",
        status_code=status.HTTP_204_NO_CONTENT, 
        summary="Удалить задачу по ее ID.",
        tags=["Tasks"])
async def delete_task(task_id : int):
    try:
        await AsyncORM.delete_task(task_id)
        return  
    except HTTPException:
        raise