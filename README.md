# Task Tracker API

Простой REST API сервис для управления списком задач. Построен на FastAPI с использованием SQLAlchemy и SQLite.

## Основные возможности
- **CRUD операции**: Создание, чтение, обновление и удаление задач.
- **Фильтрация**: Поиск задач по статусу и приоритету.
- **Поиск**: Поиск по подстроке в названии (`title`).
- **Пагинация**: Поддержка параметров `page` и `per_page`.
- **Валидация**: Использование Pydantic схем и Enum для статусов/приоритетов.
- **Docker**: Проект полностью контейнеризирован.

## Стек технологий
- **Backend**: Python 3.11, FastAPI
- **Database**: SQLite, SQLAlchemy (ORM)
- **Validation**: Pydantic v2
- **DevOps**: Docker, Docker Compose

## Как запустить проект

### 1. Локально (без Docker)
1. Установите зависимости:
   ```bash
   pip install -r requirements.txt

2. запустите сервер
- через консоль: uvicorn app.main:app --reload
- Через Docker Compose: docker-compose up --build
Сервис будет доступен по адресу: http://localhost:8000
# Документация API
После запуска проекта интерактивная документация доступна здесь:
Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

# Структура проекта
- **app/main.py** — точка входа в приложение.
- **app/models.py** — описание моделей SQLAlchemy.
- **app/schemas.py** — Pydantic схемы для валидации данных.
- **app/database.py** — настройка подключения к БД.
- **app/enum.py** — перечисления для статусов и приоритетов.

| №  | Требование                                          | Место в проекте (файл: пояснение)                                                                          |
|----|-----------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| 1  | Основные типы данных и их методы                    | `models.py`, `schemas.py`, `enum.py`                                                                       |
| 2  | Обработка ошибок                                    | `routers/tasks.py`, (HTTPException 404)                                                                    |
| 3  | Работа с файлами, менеджер контекста, декораторы    | *в `utils.py`* (декоратор `@timer`, контекстный менеджер для чтения бд и записи в бд и чтение джейсона)    |
| 4  | GIL                                                 | *теоретически* (устно: GIL ограничивает CPU-потоки, FastAPI использует asyncio)                            |
| 5  | Инкапсуляция, абстракция, наследование, полиморфизм | `models.py` (наследование Base), `schemas.py` (TaskCreate → TaskBase), инкапсуляция полей                  |
| 6  | Классы, магические методы, миксины                  | `models.py` (`__repr__`), миксин `TimestampMixin` будет в `utils.py`                                       |
| 7  | GC (сборщик мусора)                                 | *теоретически* (подсчёт ссылок + циклический сборщик в CPython)                                            |
| 8  | Базы данных / SQL                                   | `database.py`, `models.py`, `routers/tasks.py` (SQLAlchemy ORM)                                            |
| 9  | ACID                                                | SQLite + SQLAlchemy: атомарность (`commit`), согласованность (`nullable=False`), изоляция, долговечность   |
| 10 | SELECT, INSERT, JOIN                                | SELECT\INSERT: `routers/tasks.py`; JOIN (при необходимости добавим, можно добавить связь с пользователями) |
| 11 | LIMIT и OFFSET                                      | `routers/tasks.py` (`offset(skip).limit(per_page)`) – пагинация через page/per_page                        |
| 12 | FastAPI                                             | `main.py`, `routers/tasks.py` (декораторы, Depends, Query, автоматическая валидация)                       |
| 13 | WSGI / ASGI                                         | `main.py` (запуск через uvicorn – ASGI сервер)                                                             |
| 14 | Git                                                 | `.gitignore`, история коммитов на GitHub                                                                   |
| 15 | Docker                                              | `Dockerfile`, `docker-compose.yml` (запуск: `docker-compose up --build`)                                   |
| 16 | Тестирование                                        | * в `tests/`* (pytest + TestClient для эндпоинтов)                                                    |
| 17 | SOLID, DRY                                          | Архитектура: разделение routers/models/schemas (S), dependency injection (D), DRY: enum, TaskBase          |
| 20 | Выполнить тестовое                                  | Весь проект (CRUD, фильтрация, пагинация, валидация)                                                       |
| 21 | Рефакторинг на GitHub                               | Исходный код (выделение констант, enum, схем, dependency injection)                                        |
|----|-----------------------------------------------------| ---------------------------------------------------------------------------------------------------------- |

Как проверить?
Пагинация → routers/tasks.py (параметры page, per_page).

Фильтрация → routers/tasks.py (status, priority, title).

Сортировка → routers/tasks.py (sort_by_date, sort_by_priority).

Обработка ошибок → routers/tasks.py (HTTPException 404).

Примечание для проверяющего: пункты 3 (декораторы/контекстные менеджеры), 6 (миксины) и 16 (тесты) будут добавлены в ближайшее время в файлы utils.py и tests/ соответственно. Остальные требования уже выполнены в представленном коде.
