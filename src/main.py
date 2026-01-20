"""Основной модуль приложения с CLI интерфейсом."""
from src.models.task import TaskStatus, Priority
from src.repositories.user_repository import UserRepository
from src.repositories.project_repository import ProjectRepository
from src.repositories.task_repository import TaskRepository
from src.services.user_service import UserService
from src.services.project_service import ProjectService
from src.services.task_service import TaskService


class TaskManagerCLI:
    """Консольный интерфейс для системы управления задачами."""
    
    def __init__(
        self,
        project_service: ProjectService,
        task_service: TaskService,
        user_service: UserService
    ):
        """Инициализация CLI.
        
        Args:
            project_service: Сервис проектов
            task_service: Сервис задач
            user_service: Сервис пользователей
        """
        self.project_service = project_service
        self.task_service = task_service
        self.user_service = user_service
        self.current_user_id = None
    
    def run(self):
        """Запустить CLI."""
        print("=== Система управления задачами ===")
        print()
        
        # Демонстрационные данные
        self._initialize_demo_data()
        
        while True:
            self.show_menu()
            choice = input("\nВыберите действие: ").strip()
            
            if choice == "1":
                self.handle_create_project()
            elif choice == "2":
                self.handle_create_task()
            elif choice == "3":
                self.handle_assign_task()
            elif choice == "4":
                self.handle_update_status()
            elif choice == "5":
                self.handle_list_projects()
            elif choice == "6":
                self.handle_list_tasks()
            elif choice == "7":
                self.handle_project_progress()
            elif choice == "0":
                print("До свидания!")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")
    
    def show_menu(self):
        """Показать главное меню."""
        print("\n" + "="*50)
        print("1. Создать проект")
        print("2. Создать задачу")
        print("3. Назначить задачу")
        print("4. Изменить статус задачи")
        print("5. Список проектов")
        print("6. Список задач проекта")
        print("7. Прогресс проекта")
        print("0. Выход")
        print("="*50)
    
    def handle_create_project(self):
        """Обработать создание проекта."""
        print("\n--- Создание проекта ---")
        name = input("Название проекта: ").strip()
        description = input("Описание: ").strip()
        
        try:
            project = self.project_service.create_project(
                name=name,
                description=description,
                owner_id=self.current_user_id
            )
            print(f"✓ Проект создан: {project}")
        except ValueError as e:
            print(f"✗ Ошибка: {e}")
    
    def handle_create_task(self):
        """Обработать создание задачи."""
        print("\n--- Создание задачи ---")
        title = input("Заголовок: ").strip()
        description = input("Описание: ").strip()
        project_id = int(input("ID проекта: ").strip())
        
        print("Приоритет: 1-LOW, 2-MEDIUM, 3-HIGH, 4-CRITICAL")
        priority_choice = input("Выберите (по умолчанию MEDIUM): ").strip()
        priority_map = {"1": Priority.LOW, "2": Priority.MEDIUM, 
                       "3": Priority.HIGH, "4": Priority.CRITICAL}
        priority = priority_map.get(priority_choice, Priority.MEDIUM)
        
        try:
            task = self.task_service.create_task(
                title=title,
                description=description,
                project_id=project_id,
                priority=priority
            )
            print(f"✓ Задача создана: {task}")
        except ValueError as e:
            print(f"✗ Ошибка: {e}")
    
    def handle_assign_task(self):
        """Обработать назначение задачи."""
        print("\n--- Назначение задачи ---")
        task_id = int(input("ID задачи: ").strip())
        user_id = int(input("ID пользователя: ").strip())
        
        try:
            self.task_service.assign_task(task_id, user_id)
            print("✓ Задача назначена")
        except ValueError as e:
            print(f"✗ Ошибка: {e}")
    
    def handle_update_status(self):
        """Обработать изменение статуса."""
        print("\n--- Изменение статуса ---")
        task_id = int(input("ID задачи: ").strip())
        
        print("Статус: 1-NEW, 2-IN_PROGRESS, 3-IN_REVIEW, 4-COMPLETED")
        status_choice = input("Выберите: ").strip()
        status_map = {
            "1": TaskStatus.NEW,
            "2": TaskStatus.IN_PROGRESS,
            "3": TaskStatus.IN_REVIEW,
            "4": TaskStatus.COMPLETED
        }
        status = status_map.get(status_choice)
        
        if not status:
            print("✗ Неверный выбор статуса")
            return
        
        try:
            self.task_service.update_task_status(task_id, status)
            print("✓ Статус обновлен")
        except ValueError as e:
            print(f"✗ Ошибка: {e}")
    
    def handle_list_projects(self):
        """Показать список проектов."""
        print("\n--- Список проектов ---")
        projects = self.project_service.get_all_projects()
        
        if not projects:
            print("Проектов нет")
            return
        
        for project in projects:
            print(f"\n{project}")
    
    def handle_list_tasks(self):
        """Показать задачи проекта."""
        print("\n--- Задачи проекта ---")
        project_id = int(input("ID проекта: ").strip())
        
        try:
            tasks = self.task_service.get_tasks_by_project(project_id)
            
            if not tasks:
                print("Задач нет")
                return
            
            for task in tasks:
                print(f"\n{task}")
        except Exception as e:
            print(f"✗ Ошибка: {e}")
    
    def handle_project_progress(self):
        """Показать прогресс проекта."""
        print("\n--- Прогресс проекта ---")
        project_id = int(input("ID проекта: ").strip())
        
        try:
            progress = self.project_service.get_project_progress(project_id)
            print(f"Прогресс выполнения: {progress:.1f}%")
        except ValueError as e:
            print(f"✗ Ошибка: {e}")
    
    def _initialize_demo_data(self):
        """Инициализировать демонстрационные данные."""
        # Создание пользователей
        admin = self.user_service.register_user(
            name="Администратор",
            email="admin@example.com",
            role="admin"
        )
        user1 = self.user_service.register_user(
            name="Иван Иванов",
            email="ivan@example.com"
        )
        user2 = self.user_service.register_user(
            name="Мария Петрова",
            email="maria@example.com"
        )
        
        self.current_user_id = admin.id
        
        # Создание проекта
        project = self.project_service.create_project(
            name="Разработка веб-приложения",
            description="Система управления задачами",
            owner_id=admin.id
        )
        
        # Создание задач
        task1 = self.task_service.create_task(
            title="Проектирование архитектуры",
            description="Разработать UML-диаграммы",
            project_id=project.id,
            priority=Priority.HIGH
        )
        
        task2 = self.task_service.create_task(
            title="Реализация моделей данных",
            description="Создать классы User, Project, Task",
            project_id=project.id,
            priority=Priority.MEDIUM
        )
        
        # Назначение задач
        self.task_service.assign_task(task1.id, user1.id)
        self.task_service.assign_task(task2.id, user2.id)
        
        # Изменение статусов
        self.task_service.update_task_status(task1.id, TaskStatus.COMPLETED)
        
        print("Демонстрационные данные загружены!")
        print(f"Вы вошли как: {admin.name}")


def main():
    """Точка входа приложения."""
    # Инициализация репозиториев
    user_repo = UserRepository()
    project_repo = ProjectRepository()
    task_repo = TaskRepository()
    
    # Инициализация сервисов
    user_service = UserService(user_repo)
    project_service = ProjectService(project_repo, user_repo)
    task_service = TaskService(task_repo, project_repo, user_repo)
    
    # Запуск CLI
    cli = TaskManagerCLI(project_service, task_service, user_service)
    cli.run()


if __name__ == "__main__":
    main()
