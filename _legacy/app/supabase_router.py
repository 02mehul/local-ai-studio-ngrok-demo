from fastapi import APIRouter, HTTPException, Query, Request
from typing import List, Optional
from .models import TodoItem, TodoCreate, TodoUpdate
from . import storage

router = APIRouter()

# Helper to parse "eq.X" style filters
def parse_id_filter(id_param: str) -> int:
    if id_param.startswith("eq."):
        try:
            return int(id_param.split("eq.")[1])
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid ID format. Use 'eq.<integer>'")
    try:
        return int(id_param)
    except ValueError:
       # If it's not eq.X, maybe it's just X. If fails, error.
       raise HTTPException(status_code=400, detail="Invalid ID format. Use 'eq.<integer>'")

@router.get("/todos", response_model=List[TodoItem])
def get_todos(select: Optional[str] = Query(None)):
    # In a real PostgREST, select would filter columns. Here we just return full objects.
    return storage.get_todos()

@router.post("/todos", response_model=List[TodoItem], status_code=201)
def create_todo(todo: TodoCreate, request: Request):
    # PostgREST accepts object or array of objects. We'll handle single object for now as per model.
    # Note: AI Studio might send array if it thinks it's bulk.
    # But schema says TodoCreate is object.
    
    new_id = storage.get_next_id()
    new_item = TodoItem(id=new_id, **todo.dict())
    storage.add_todo(new_item)
    
    # Supabase returns array of created items
    return [new_item]

@router.patch("/todos", response_model=List[TodoItem])
def update_todo(todo: TodoUpdate, id: str = Query(..., description="Filter by ID, e.g. 'eq.1'")):
    target_id = parse_id_filter(id)
    updated_items = []
    
    found = False
    for item in storage.get_todos():
        if item.id == target_id:
            if todo.title is not None:
                item.title = todo.title
            if todo.done is not None:
                item.done = todo.done
            updated_items.append(item)
            found = True
            break # ID is unique
            
    if not found:
        # PostgREST returns empty list if no match, not 404 usually, but for AI clarity...
        # We'll return empty list.
        return []
        
    return updated_items

@router.delete("/todos", response_model=List[TodoItem])
def delete_todo(id: str = Query(..., description="Filter by ID, e.g. 'eq.1'")):
    target_id = parse_id_filter(id)
    deleted_items = []
    
    # We need to modify the list in place or replace it
    # accessing storage.todos directly since it's a list reference
    todos = storage.get_todos()
    
    initial_len = len(todos)
    # Filter out the item
    item_to_delete = next((x for x in todos if x.id == target_id), None)
    
    if item_to_delete:
        deleted_items.append(item_to_delete)
        todos.remove(item_to_delete)
        
    return deleted_items
