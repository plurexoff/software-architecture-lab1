"""Репозиторий для работы с пользователями."""
from typing import Optional
from .base import InMemoryRepository
from src.models.user import User


class UserRepository(InMemoryRepository[User]):
    """Репозиторий пользователей с дополнительными методами."""
    
    def find_by_email(self, email: str) -> Optional[User]:
        """Найти пользователя по email.
        
        Args:
            email: Email для поиска
        
        Returns:
            Пользователь или None
        """
        for user in self.get_all():
            if user.email == email:
                return user
        return None
