from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str
    done: bool = False

class TodoUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None

class TodoItem(TodoCreate):
    id: int
