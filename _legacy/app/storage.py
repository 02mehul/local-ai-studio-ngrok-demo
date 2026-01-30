from typing import List
from .models import TodoItem

# In-memory store
todos: List[TodoItem] = []
current_id = 1

def get_todos() -> List[TodoItem]:
    return todos

def add_todo(todo: TodoItem):
    todos.append(todo)

def get_next_id() -> int:
    global current_id
    id_val = current_id
    current_id += 1
    return id_val

def clear_todos():
    global todos, current_id
    todos = []
    current_id = 1
