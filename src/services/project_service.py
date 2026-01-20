"""Сервис для работы с проектами."""
from typing import List, Optional
from src.models.project import Project
from src.repositories.project_repository import ProjectRepository
from src.repositories.user_repository import UserRepository


class ProjectService:
    """Сервис для управления проектами."""
    
    def __init__(self, project_repo: ProjectRepository, user_repo: UserRepository):
        """Инициализация сервиса.
        
        Args:
            project_repo: Репозиторий проектов
            user_repo: Репозиторий пользователей
        """
        self.project_repo = project_repo
        self.user_repo = user_repo
    
    def create_project(self, name: str, description: str, owner_id: int) -> Project:
        """Создать новый проект.
        
        Args:
            name: Название проекта
            description: Описание проекта
            owner_id: ID владельца
        
        Returns:
            Созданный проект
        
        Raises:
            ValueError: Если владелец не существует
        """
        # Проверка существования владельца
        owner = self.user_repo.get_by_id(owner_id)
        if not owner:
            raise ValueError(f"Пользователь с ID {owner_id} не найден")
        
        # Валидация данных
        if not name or len(name.strip()) == 0:
            raise ValueError("Название проекта не может быть пустым")
        
        # Создание проекта
        project = Project(
            project_id=None,
            name=name,
            description=description,
            owner_id=owner_id
        )
        self.project_repo.add(project)
        
        return project
    
    def get_project(self, project_id: int) -> Optional[Project]:
        """Получить проект по ID.
        
        Args:
            project_id: ID проекта
        
        Returns:
            Проект или None
        """
        return self.project_repo.get_by_id(project_id)
    
    def get_all_projects(self) -> List[Project]:
        """Получить все проекты.
        
        Returns:
            Список проектов
        """
        return self.project_repo.get_all()
    
    def delete_project(self, project_id: int, user_id: int) -> None:
        """Удалить проект.
        
        Args:
            project_id: ID проекта
            user_id: ID пользователя, запрашивающего удаление
        
        Raises:
            ValueError: Если проект не найден или пользователь не владелец
        """
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError(f"Проект с ID {project_id} не найден")
        
        # Проверка прав доступа
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ValueError(f"Пользователь с ID {user_id} не найден")
        
        if project.owner_id != user_id and user.role != "admin":
            raise ValueError("Только владелец или администратор может удалить проект")
        
        self.project_repo.delete(project_id)
    
    def get_project_progress(self, project_id: int) -> float:
        """Получить прогресс выполнения проекта.
        
        Args:
            project_id: ID проекта
        
        Returns:
            Процент выполнения (0-100)
        
        Raises:
            ValueError: Если проект не найден
        """
        project = self.project_repo.get_by_id(project_id)
        if not project:
            raise ValueError(f"Проект с ID {project_id} не найден")
        
        return project.calculate_progress()
