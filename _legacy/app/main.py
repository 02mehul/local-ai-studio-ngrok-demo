from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .models import TodoItem, TodoCreate, TodoUpdate
from . import storage
from . import supabase_router

app = FastAPI(
    title="Local AI Studio Demo API",
    description="A simple backend to demonstrate Google AI Studio integration via ngrok.",
    version="1.0.0",
)

# CORS: Allow everything for demo purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the Supabase-compatible router
app.include_router(supabase_router.router, prefix="/rest/v1", tags=["Supabase"])

# --- Legacy / Simple Frontend Routes (keeping for backward compatibility) ---

@app.get("/health")
def health_check():
    return {"ok": True}

@app.get("/todos", response_model=List[TodoItem])
def get_todos():
    return storage.get_todos()

@app.post("/todos", response_model=TodoItem)
def create_todo(todo: TodoCreate):
    new_id = storage.get_next_id()
    new_todo = TodoItem(id=new_id, **todo.dict())
    storage.add_todo(new_todo)
    return new_todo

@app.patch("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, update: TodoUpdate):
    for item in storage.get_todos():
        if item.id == todo_id:
            if update.title is not None:
                item.title = update.title
            if update.done is not None:
                item.done = update.done
            return item
    raise HTTPException(status_code=404, detail="Todo not found")
