from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import TaskModel
from app.schemas import Task, TaskCreate, TaskUpdate
from app.models_enums import TaskStatus, TaskPriority

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

def get_task_or_404(id: int, db: Session = Depends(get_db)) -> Task:
    task = db.query(TaskModel).filter(TaskModel.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail='задача не найдена')
    return task

@router.post('/', response_model=Task, status_code=201)
async def create_task(task: TaskCreate, db: Session = Depends(get_db)) -> Task:
    db_task = TaskModel(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get('/', response_model=list[Task])
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
    order_by_clauses = []
    if sort_by_date:
        order_by_clauses.append(
            TaskModel.created_at.desc() if sort_by_date == "desc" else TaskModel.created_at.asc()
        )
    if sort_by_priority:
        order_by_clauses.append(
            TaskModel.priority.desc() if sort_by_priority == "desc" else TaskModel.priority.asc()
        )
    if order_by_clauses:
        query = tasks.order_by(*order_by_clauses)
    else:
        query = tasks.order_by(TaskModel.created_at.desc())
    skip = (page - 1) * per_page
    return query.offset(skip).limit(per_page).all()

@router.get('/{id}', response_model=Task)
async def get_task(id: int, db: Session = Depends(get_db)) -> Task:
    return get_task_or_404(id, db)

@router.put('/{id}', response_model=Task)
async def update_task(id: int, task_update: TaskUpdate, db: Session = Depends(get_db)) -> Task:
    db_task = get_task_or_404(id, db)
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete('/{id}', response_model=Task)
async def delete_task(id: int, db: Session = Depends(get_db)) -> Task:
    db_task = db.query(TaskModel).filter(TaskModel.id == id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail='задача для удаления не найдена')
    db.delete(db_task)
    db.commit()
    return db_task