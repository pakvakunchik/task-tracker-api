import json
import time
from app.database import engine, session_local
from sqlalchemy.ext.automap import automap_base
from loguru import logger

logger.add("app.log", level="INFO")

'''пример работы с файлами и контекстным менеджером'''
Base = automap_base()
def write_db():
    Base.prepare(autoload_with=engine)
    Tasks = Base.classes.tasks
    try:
        with session_local() as session:
            rows = session.query(Tasks).all()
            data = []
            for row in rows:
                to_dict = dict(row.__dict__)
                to_dict.pop("_sa_instance_state", None)
                data.append(to_dict)
        with open("tasks.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, default=str)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(e)

def read_db():
    with open("tasks.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        print(data)
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

