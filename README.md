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


