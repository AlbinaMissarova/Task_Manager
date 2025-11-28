# прослойка между эндпоинтами и моделями БД
from typing import Optional
from pydantic import BaseModel, ConfigDict

# DTO - Data Transfer Object - объект передачи данных

# добавление задачи - не должно содержаться ID - его присваивает БД
class TaskAddDTO(BaseModel):
    # Название задачи
    title: str
    # Описание задачи
    description: Optional[str] = None
    # Статус (выполнены/не выполнено)
    completed: bool 

    model_config = ConfigDict(from_attributes=True)

# изменение задачи - все поля опциональны
class TaskUpdateDTO(BaseModel):
    # Название задачи
    title: Optional[str] = None
    # Описание задачи
    description: Optional[str] = None
    # Статус (выполнены/не выполнено)
    completed: Optional[bool]  = None

    model_config = ConfigDict(from_attributes=True)

# задача со всеми полями
class TaskDTO(TaskAddDTO):
    # Номер задачи
    task_id: int
