from fastapi import FastAPI

import app.routers.tasks as tasks
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(tasks.app)


