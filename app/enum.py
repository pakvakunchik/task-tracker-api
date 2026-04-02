import enum
class TaskStatus(enum.Enum):
    todo = 'todo'
    in_progress = 'in_progress'
    complete = 'complete'

class TaskPriority(enum.Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'