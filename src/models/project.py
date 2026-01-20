"""Модель проекта."""
from datetime import datetime
from typing import List, Optional


class Project:
    """Класс для представления проекта."""
    
    def __init__(
        self,
        project_id: int,
        name: str,
        description: str,
        owner_id: int
    ):
        """Инициализация проекта.
        
        Args:
            project_id: Уникальный идентификатор
            name: Название проекта
            description: Описание проекта
            owner_id: ID владельца проекта
        """
        self.id = project_id
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.created_at = datetime.now()
        self.status = "active"
        self.tasks: List = []  # Список задач проекта
    
    def add_task(self, task) -> None:
        """Добавить задачу в проект.
        
        Args:
            task: Объект задачи
        """
        if task not in self.tasks:
            self.tasks.append(task)
    
    def calculate_progress(self) -> float:
        """Рассчитать процент выполнения проекта.
        
        Returns:
            Процент выполненных задач (0-100)
        """
        if not self.tasks:
            return 0.0
        
        from .task import TaskStatus
        completed = sum(1 for t in self.tasks if t.status == TaskStatus.COMPLETED)
        return (completed / len(self.tasks)) * 100
    
    def __str__(self) -> str:
        return (
            f"Project(id={self.id}, name={self.name}, "
            f"status={self.status}, tasks={len(self.tasks)}, "
            f"progress={self.calculate_progress():.1f}%)"
        )
    
    def __repr__(self) -> str:
        return self.__str__()
