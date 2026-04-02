from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models import TaskModel
from app.schemas import Task, TaskCreate, TaskUpdate
from app.enum import TaskStatus, TaskPriority

app = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@app.post('/tasks', response_model=Task, status_code=201)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)) -> Task:
    db_task = TaskModel(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.get('/tasks', response_model=list[Task])
async def get_tasks(
        db: Session = Depends(get_db),
        status: Optional[TaskStatus] = Query(None, description='фильтр по статусу'),
        priority: Optional[TaskPriority] = Query(None, description='фильтр по приоритету'),
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=100),
        title: Optional[str] = Query(None, description='Поиск по названию'),
        sort_by_date: Optional[str] = Query(None, regex='^(asc|desc)$'),
        sort_by_priority: Optional[str] = Query(None, regex='^(asc|desc)$')
) -> List[Task]:
    tasks = db.query(TaskModel)
    if title:
        tasks = tasks.filter(TaskModel.title.ilike(f'%{title}%'))
    if status:
        tasks = tasks.filter(TaskModel.status == status.value)
    if priority:
        tasks = tasks.filter(TaskModel.priority == priority.value)
    if sort_by_date == 'desc':
        tasks = tasks.order_by(TaskModel.created_at.desc())
    else:
        tasks = tasks.order_by(TaskModel.created_at.asc())
    if sort_by_priority == 'desc':
        tasks = tasks.order_by(TaskModel.priority.desc())
    else:
        tasks = tasks.order_by(TaskModel.priority.asc())
    skip = (page - 1) * per_page
    return tasks.offset(skip).limit(per_page).all()

@app.get('/tasks/{id}', response_model=Task)
async def get_task(id: int, db: Session = Depends(get_db)) -> Task:
    task = db.query(TaskModel).filter(TaskModel.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail='задача не найдена')
    return task

@app.put('/tasks/{id}', response_model=Task)
async def update_task(id: int, task: TaskUpdate, db: Session = Depends(get_db)) -> Task:
    db_task = db.query(TaskModel).filter(TaskModel.id == id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail='задача для обновления не найдена')
    db_task.title = task.title
    db_task.description = task.description
    db_task.status = task.status
    db_task.priority = task.priority
    db.commit()
    db.refresh(db_task)
    return db_task

@app.delete('/tasks/{id}', response_model=Task)
async def delete_task(id: int, db: Session = Depends(get_db)) -> Task:
    db_task = db.query(TaskModel).filter(TaskModel.id == id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail='задача для удаления не найдена')
    db.delete(db_task)
    db.commit()
    return db_task
