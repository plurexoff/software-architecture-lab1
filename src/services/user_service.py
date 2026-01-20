"""Сервис для работы с пользователями."""
from typing import List, Optional
from src.models.user import User
from src.repositories.user_repository import UserRepository


class UserService:
    """Сервис для управления пользователями."""
    
    def __init__(self, user_repo: UserRepository):
        """Инициализация сервиса.
        
        Args:
            user_repo: Репозиторий пользователей
        """
        self.user_repo = user_repo
    
    def register_user(self, name: str, email: str, role: str = "member") -> User:
        """Зарегистрировать нового пользователя.
        
        Args:
            name: Имя пользователя
            email: Email пользователя
            role: Роль пользователя
        
        Returns:
            Созданный пользователь
        
        Raises:
            ValueError: Если email уже существует
        """
        # Проверка на существование пользователя с таким email
        existing_user = self.user_repo.find_by_email(email)
        if existing_user:
            raise ValueError(f"Пользователь с email {email} уже существует")
        
        # Валидация роли
        if role not in ["admin", "member"]:
            raise ValueError("Роль должна быть 'admin' или 'member'")
        
        # Создание пользователя
        user = User(user_id=None, name=name, email=email, role=role)
        self.user_repo.add(user)
        
        return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID.
        
        Args:
            user_id: ID пользователя
        
        Returns:
            Пользователь или None
        """
        return self.user_repo.get_by_id(user_id)
    
    def get_all_users(self) -> List[User]:
        """Получить всех пользователей.
        
        Returns:
            Список пользователей
        """
        return self.user_repo.get_all()
