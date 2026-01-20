# UML-диаграмма классов

## Диаграмма классов системы управления задачами

```mermaid
classDiagram
    %% Domain Layer - Модели данных
    class User {
        -int id
        -str name
        -str email
        -str role
        +__init__(id, name, email, role)
        +__str__() str
    }

    class Project {
        -int id
        -str name
        -str description
        -datetime created_at
        -str status
        -int owner_id
        -List~Task~ tasks
        +__init__(id, name, description, owner_id)
        +add_task(task) void
        +calculate_progress() float
        +__str__() str
    }

    class Task {
        -int id
        -str title
        -str description
        -Priority priority
        -TaskStatus status
        -int project_id
        -int assignee_id
        -datetime created_at
        +__init__(id, title, description, project_id)
        +assign_to(user_id) void
        +change_status(status) void
        +__str__() str
    }

    class TaskStatus {
        <<enumeration>>
        NEW
        IN_PROGRESS
        IN_REVIEW
        COMPLETED
    }

    class Priority {
        <<enumeration>>
        LOW
        MEDIUM
        HIGH
        CRITICAL
    }

    %% Data Access Layer - Репозитории
    class IRepository~T~ {
        <<abstract>>
        +add(entity: T) void
        +get_by_id(id: int) T
        +get_all() List~T~
        +update(entity: T) void
        +delete(id: int) void
    }

    class InMemoryRepository~T~ {
        -Dict~int, T~ _storage
        -int _next_id
        +add(entity: T) void
        +get_by_id(id: int) T
        +get_all() List~T~
        +update(entity: T) void
        +delete(id: int) void
    }

    class UserRepository {
        +find_by_email(email: str) User
    }

    class ProjectRepository {
        +find_by_owner(owner_id: int) List~Project~
    }

    class TaskRepository {
        +find_by_project(project_id: int) List~Task~
        +find_by_assignee(assignee_id: int) List~Task~
        +find_by_status(status: TaskStatus) List~Task~
    }

    %% Business Logic Layer - Сервисы
    class UserService {
        -UserRepository user_repo
        +__init__(user_repo)
        +register_user(name, email, role) User
        +get_user(user_id) User
        +get_all_users() List~User~
    }

    class ProjectService {
        -ProjectRepository project_repo
        -UserRepository user_repo
        +__init__(project_repo, user_repo)
        +create_project(name, description, owner_id) Project
        +get_project(project_id) Project
        +get_all_projects() List~Project~
        +delete_project(project_id, user_id) void
        +get_project_progress(project_id) float
    }

    class TaskService {
        -TaskRepository task_repo
        -ProjectRepository project_repo
        -UserRepository user_repo
        +__init__(task_repo, project_repo, user_repo)
        +create_task(title, description, project_id) Task
        +assign_task(task_id, user_id) void
        +update_task_status(task_id, status) void
        +get_task(task_id) Task
        +get_tasks_by_project(project_id) List~Task~
        +get_tasks_by_user(user_id) List~Task~
    }

    %% Presentation Layer
    class TaskManagerCLI {
        -ProjectService project_service
        -TaskService task_service
        -UserService user_service
        +__init__(project_service, task_service, user_service)
        +run() void
        +show_menu() void
        +handle_create_project() void
        +handle_create_task() void
        +handle_list_tasks() void
    }

    %% Связи между классами
    Project "1" --o "*" Task : contains
    User "1" -- "*" Task : assigned to
    User "1" -- "*" Project : owns
    Task --> TaskStatus : uses
    Task --> Priority : uses

    %% Наследование репозиториев
    IRepository <|-- InMemoryRepository : implements
    InMemoryRepository <|-- UserRepository : extends
    InMemoryRepository <|-- ProjectRepository : extends
    InMemoryRepository <|-- TaskRepository : extends

    %% Зависимости сервисов
    UserService --> UserRepository : uses
    ProjectService --> ProjectRepository : uses
    ProjectService --> UserRepository : uses
    TaskService --> TaskRepository : uses
    TaskService --> ProjectRepository : uses
    TaskService --> UserRepository : uses

    %% Зависимости CLI
    TaskManagerCLI --> ProjectService : uses
    TaskManagerCLI --> TaskService : uses
    TaskManagerCLI --> UserService : uses
```

## Описание основных классов

### Domain Layer (Модели)

#### User
Представляет пользователя системы с уникальным ID, именем, email и ролью.

#### Project
Контейнер для задач, содержит метаданные проекта и методы для управления задачами.

#### Task
Основная единица работы, содержит всю информацию о задаче.

#### TaskStatus и Priority
Перечисления для типобезопасного управления статусами и приоритетами.

### Data Access Layer (Репозитории)

#### IRepository<T>
Абстрактный базовый класс, определяющий общий интерфейс для CRUD-операций.

#### InMemoryRepository<T>
Конкретная реализация, хранящая данные в памяти через словарь.

#### UserRepository, ProjectRepository, TaskRepository
Специализированные репозитории с дополнительными методами для поиска и фильтрации.

### Business Logic Layer (Сервисы)

#### UserService
Управляет пользователями: регистрация, получение, валидация.

#### ProjectService
Реализует бизнес-логику для проектов: создание, удаление, расчет прогресса.

#### TaskService
Обеспечивает всю логику работы с задачами: создание, назначение, изменение статуса.

### Presentation Layer

#### TaskManagerCLI
Консольный интерфейс, координирующий взаимодействие пользователя с сервисами.

## Основные взаимосвязи

- **Ассоциация**: User связан с Task и Project
- **Композиция**: Project содержит Task
- **Наследование**: Специализированные репозитории наследуются от InMemoryRepository
- **Зависимость**: Сервисы зависят от репозиториев (через Dependency Injection)
