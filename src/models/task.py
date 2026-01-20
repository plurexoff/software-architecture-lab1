"""Модель задачи."""
from datetime import datetime
from enum import Enum
from typing import Optional


class TaskStatus(Enum):
    """Перечисление статусов задачи."""
    NEW = "new"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    COMPLETED = "completed"


class Priority(Enum):
    """Перечисление приоритетов."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Task:
    """Класс для представления задачи."""
    
    def __init__(
        self,
        task_id: int,
        title: str,
        description: str,
        project_id: int,
        priority: Priority = Priority.MEDIUM
    ):
        """Инициализация задачи.
        
        Args:
            task_id: Уникальный идентификатор
            title: Заголовок задачи
            description: Описание задачи
            project_id: ID проекта
            priority: Приоритет задачи
        """
        self.id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.status = TaskStatus.NEW
        self.project_id = project_id
        self.assignee_id: Optional[int] = None
        self.created_at = datetime.now()
    
    def assign_to(self, user_id: int) -> None:
        """Назначить задачу пользователю.
        
        Args:
            user_id: ID пользователя
        """
        self.assignee_id = user_id
    
    def change_status(self, status: TaskStatus) -> None:
        """Изменить статус задачи.
        
        Args:
            status: Новый статус
        """
        self.status = status
    
    def __str__(self) -> str:
        return (
            f"Task(id={self.id}, title={self.title}, "
            f"status={self.status.value}, priority={self.priority.value}, "
            f"assignee={self.assignee_id})"
        )
    
    def __repr__(self) -> str:
        return self.__str__()
