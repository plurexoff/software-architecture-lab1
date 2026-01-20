# UML-диаграмма последовательностей

## Сценарий 1: Создание новой задачи

```mermaid
sequenceDiagram
    actor User as Пользователь
    participant CLI as TaskManagerCLI
    participant TS as TaskService
    participant PR as ProjectRepository
    participant UR as UserRepository
    participant TR as TaskRepository
    participant Task as Task

    User->>CLI: Выбрать "Создать задачу"
    CLI->>User: Запросить данные задачи
    User->>CLI: Ввести данные (заголовок, описание, project_id)
    
    CLI->>TS: create_task(title, description, project_id)
    
    %% Проверка существования проекта
    TS->>PR: get_by_id(project_id)
    alt Проект найден
        PR-->>TS: Project
        
        %% Создание задачи
        TS->>Task: __init__(id, title, description, project_id)
        Task-->>TS: task
        
        %% Сохранение в репозиторий
        TS->>TR: add(task)
        TR-->>TS: void
        
        TS-->>CLI: task
        CLI->>User: Отобразить успех + данные задачи
    else Проект не найден
        PR-->>TS: None
        TS-->>CLI: Error("Проект не найден")
        CLI->>User: Отобразить ошибку
    end
```

## Сценарий 2: Назначение задачи исполнителю

```mermaid
sequenceDiagram
    actor User as Пользователь
    participant CLI as TaskManagerCLI
    participant TS as TaskService
    participant TR as TaskRepository
    participant UR as UserRepository
    participant Task as Task

    User->>CLI: Выбрать "Назначить задачу"
    CLI->>User: Запросить task_id и user_id
    User->>CLI: Ввести task_id и user_id
    
    CLI->>TS: assign_task(task_id, user_id)
    
    %% Проверка существования задачи
    TS->>TR: get_by_id(task_id)
    TR-->>TS: task
    
    %% Проверка существования пользователя
    TS->>UR: get_by_id(user_id)
    alt Пользователь найден
        UR-->>TS: user
        
        %% Назначение задачи
        TS->>Task: assign_to(user_id)
        Task-->>TS: void
        
        %% Обновление в репозитории
        TS->>TR: update(task)
        TR-->>TS: void
        
        TS-->>CLI: Success
        CLI->>User: "Задача назначена"
    else Пользователь не найден
        UR-->>TS: None
        TS-->>CLI: Error("Пользователь не найден")
        CLI->>User: Отобразить ошибку
    end
```

## Сценарий 3: Изменение статуса задачи

```mermaid
sequenceDiagram
    actor User as Пользователь
    participant CLI as TaskManagerCLI
    participant TS as TaskService
    participant TR as TaskRepository
    participant Task as Task

    User->>CLI: Выбрать "Изменить статус"
    CLI->>User: Запросить task_id и новый статус
    User->>CLI: Ввести task_id и status
    
    CLI->>TS: update_task_status(task_id, status)
    
    %% Получение задачи
    TS->>TR: get_by_id(task_id)
    TR-->>TS: task
    
    %% Изменение статуса
    TS->>Task: change_status(status)
    Task-->>TS: void
    
    %% Сохранение изменений
    TS->>TR: update(task)
    TR-->>TS: void
    
    TS-->>CLI: Success
    CLI->>User: "Статус обновлен"
```

## Сценарий 4: Просмотр задач проекта с фильтрацией

```mermaid
sequenceDiagram
    actor User as Пользователь
    participant CLI as TaskManagerCLI
    participant TS as TaskService
    participant TR as TaskRepository

    User->>CLI: Выбрать "Показать задачи проекта"
    CLI->>User: Запросить project_id
    User->>CLI: Ввести project_id
    
    CLI->>TS: get_tasks_by_project(project_id)
    
    %% Запрос задач из репозитория
    TS->>TR: find_by_project(project_id)
    TR-->>TS: List[Task]
    
    TS-->>CLI: List[Task]
    
    %% Отображение задач
    loop Для каждой задачи
        CLI->>User: Отобразить task (id, title, status, assignee)
    end
```

## Описание взаимодействий

### Основные участники:
- **Пользователь** - инициирует действия
- **CLI** - обрабатывает ввод/вывод
- **Service** - реализует бизнес-логику
- **Repository** - управляет данными
- **Модель** - представляет данные

### Шаблон взаимодействия:
1. Пользователь инициирует действие через CLI
2. CLI запрашивает необходимые данные
3. CLI вызывает метод сервиса
4. Сервис валидирует и обрабатывает запрос
5. Сервис взаимодействует с репозиториями
6. Результат возвращается пользователю через CLI

### Обработка ошибок:
- Валидация входных данных в сервисах
- Проверка существования связанных сущностей
- Возврат понятных сообщений об ошибках
- Отображение ошибок пользователю через CLI
