import json
import time
from sqlalchemy.ext.automap import automap_base
from loguru import logger
from app.database import engine, Session_local
from app.models import TaskModel

logger.add("app.log", level="INFO")

'''пример работы с файлами и контекстным менеджером'''
Base = automap_base()
def write_db(filename: str = "tasks.json"):
    Base.prepare(autoload_with=engine)
    Tasks = Base.classes.tasks
    try:
        with Session_local() as session:
            tasks = session.query(TaskModel).all()
            data = []
            for task in tasks:
                task_dict = {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status.value,
                    "priority": task.priority.value,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None,
                }
                data.append(task_dict)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info(f"Exported {len(data)} tasks to {filename}")
    except Exception as e:
        logger.error(f"Export failed: {e}")


def read_db():
    with open("tasks.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        return data

'''пример понимания декоратора'''
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()  # Засекаем время
        result = func(*args, **kwargs)  # Запускаем саму функцию
        end = time.time()  # Время после выполнения
        print(f"Функция {func.__name__} работала {end - start:.2f} сек")
        return result
    return wrapper

@timer
def demo_sleep(seconds):
    time.sleep(seconds)
    return "Готово"

