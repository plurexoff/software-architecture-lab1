"""Сервис для работы с задачами."""
from typing import List, Optional
from src.models.task import Task, TaskStatus, Priority
from src.repositories.task_repository import TaskRepository
from src.repositories.project_repository import ProjectRepository
from src.repositories.user_repository import UserRepository


class TaskService:
    """Сервис для управления задачами."""
    
    def __init__(
        self,
        task_repo: TaskRepository,
        project_repo: ProjectRepository,
        user_repo: UserRepository
    ):
        """Инициализация сервиса.
        
        Args:
            task_repo: Репозиторий задач
            project_repo: Репозиторий проектов
            user_repo: Репозиторий пользователей
        """
        self.task_repo = task_repo
        self.project_repo = project_repo
        self.user_repo = user_repo
    
    def create_task(
        self,
        title: str,
        description: str,
        project_id: int,
        priority: Priority = Priority.MEDIUM
    ) -> Task:
        """Создать новую задачу.
        
        Args:
            title: Заголовок задачи
            description: Описание задачи
            project_id: ID проекта
            priority: Приоритет задачи
        
        Returns:
            Созданная задача
        
        Raises:
            ValueError: Если проект не существует
        """
        # Проверка существования проекта
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError(f"Проект с ID {project_id} не найден")
        
        # Валидация данных
        if not title or len(title.strip()) == 0:
            raise ValueError("Заголовок задачи не может быть пустым")
        
        # Создание задачи
        task = Task(
            task_id=None,
            title=title,
            description=description,
            project_id=project_id,
            priority=priority
        )
        self.task_repo.add(task)
        
        # Добавление задачи в проект
        project.add_task(task)
        self.project_repo.update(project)
        
        return task
    
    def assign_task(self, task_id: int, user_id: int) -> None:
        """Назначить задачу пользователю.
        
        Args:
            task_id: ID задачи
            user_id: ID пользователя
        
        Raises:
            ValueError: Если задача или пользователь не найдены
        """
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise ValueError(f"Задача с ID {task_id} не найдена")
        
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"Пользователь с ID {user_id} не найден")
        
        task.assign_to(user_id)
        self.task_repo.update(task)
    
    def update_task_status(self, task_id: int, status: TaskStatus) -> None:
        """Изменить статус задачи.
        
        Args:
            task_id: ID задачи
            status: Новый статус
        
        Raises:
            ValueError: Если задача не найдена
        """
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise ValueError(f"Задача с ID {task_id} не найдена")
        
        task.change_status(status)
        self.task_repo.update(task)
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Получить задачу по ID.
        
        Args:
            task_id: ID задачи
        
        Returns:
            Задача или None
        """
        return self.task_repo.get_by_id(task_id)
    
    def get_tasks_by_project(self, project_id: int) -> List[Task]:
        """Получить задачи проекта.
        
        Args:
            project_id: ID проекта
        
        Returns:
            Список задач
        """
        return self.task_repo.find_by_project(project_id)
    
    def get_tasks_by_user(self, user_id: int) -> List[Task]:
        """Получить задачи пользователя.
        
        Args:
            user_id: ID пользователя
        
        Returns:
            Список задач
        """
        return self.task_repo.find_by_assignee(user_id)
