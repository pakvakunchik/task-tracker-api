import enum
class TaskStatus(str, enum.Enum):
    todo = 'todo'
    in_progress = 'in_progress'
    complete = 'complete'

class TaskPriority(str, enum.Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'