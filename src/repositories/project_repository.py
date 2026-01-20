"""Репозиторий для работы с проектами."""
from typing import List
from .base import InMemoryRepository
from src.models.project import Project


class ProjectRepository(InMemoryRepository[Project]):
    """Репозиторий проектов с дополнительными методами."""
    
    def find_by_owner(self, owner_id: int) -> List[Project]:
        """Найти проекты по владельцу.
        
        Args:
            owner_id: ID владельца
        
        Returns:
            Список проектов
        """
        return [p for p in self.get_all() if p.owner_id == owner_id]
