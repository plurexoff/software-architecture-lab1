"""Базовый репозиторий с общим интерфейсом."""
from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic, Dict

T = TypeVar('T')


class IRepository(ABC, Generic[T]):
    """Абстрактный базовый класс репозитория."""
    
    @abstractmethod
    def add(self, entity: T) -> None:
        """Добавить сущность."""
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Получить сущность по ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Получить все сущности."""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> None:
        """Обновить сущность."""
        pass
    
    @abstractmethod
    def delete(self, entity_id: int) -> None:
        """Удалить сущность."""
        pass


class InMemoryRepository(IRepository[T]):
    """Реализация репозитория с хранением в памяти."""
    
    def __init__(self):
        self._storage: Dict[int, T] = {}
        self._next_id = 1
    
    def add(self, entity: T) -> None:
        """Добавить сущность в хранилище."""
        if hasattr(entity, 'id'):
            if entity.id is None:
                entity.id = self._next_id
                self._next_id += 1
            self._storage[entity.id] = entity
        else:
            raise ValueError("Entity must have 'id' attribute")
    
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Получить сущность по ID."""
        return self._storage.get(entity_id)
    
    def get_all(self) -> List[T]:
        """Получить все сущности."""
        return list(self._storage.values())
    
    def update(self, entity: T) -> None:
        """Обновить сущность."""
        if hasattr(entity, 'id') and entity.id in self._storage:
            self._storage[entity.id] = entity
        else:
            raise ValueError(f"Entity with id {entity.id if hasattr(entity, 'id') else 'unknown'} not found")
    
    def delete(self, entity_id: int) -> None:
        """Удалить сущность."""
        if entity_id in self._storage:
            del self._storage[entity_id]
        else:
            raise ValueError(f"Entity with id {entity_id} not found")
