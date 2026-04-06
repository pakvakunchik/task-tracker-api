from fastapi import FastAPI
from app.routers import tasks
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Task Tracker API', version='1.0')

app.include_router(tasks.router)


