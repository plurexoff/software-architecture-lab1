"""Модель пользователя системы."""

class User:
    """Класс для представления пользователя."""
    
    def __init__(self, user_id: int, name: str, email: str, role: str = "member"):
        """Инициализация пользователя.
        
        Args:
            user_id: Уникальный идентификатор
            name: Имя пользователя
            email: Email пользователя
            role: Роль (admin/member)
        """
        self.id = user_id
        self.name = name
        self.email = email
        self.role = role
    
    def __str__(self) -> str:
        return f"User(id={self.id}, name={self.name}, email={self.email}, role={self.role})"
    
    def __repr__(self) -> str:
        return self.__str__()
