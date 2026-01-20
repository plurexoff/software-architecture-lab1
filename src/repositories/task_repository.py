"""Репозиторий для работы с задачами."""
from typing import List
from .base import InMemoryRepository
from src.models.task import Task, TaskStatus


class TaskRepository(InMemoryRepository[Task]):
    """Репозиторий задач с дополнительными методами."""
    
    def find_by_project(self, project_id: int) -> List[Task]:
        """Найти задачи по проекту.
        
        Args:
            project_id: ID проекта
        
        Returns:
            Список задач
        """
        return [t for t in self.get_all() if t.project_id == project_id]
    
    def find_by_assignee(self, assignee_id: int) -> List[Task]:
        """Найти задачи по исполнителю.
        
        Args:
            assignee_id: ID исполнителя
        
        Returns:
            Список задач
        """
        return [t for t in self.get_all() if t.assignee_id == assignee_id]
    
    def find_by_status(self, status: TaskStatus) -> List[Task]:
        """Найти задачи по статусу.
        
        Args:
            status: Статус задачи
        
        Returns:
            Список задач
        """
        return [t for t in self.get_all() if t.status == status]
