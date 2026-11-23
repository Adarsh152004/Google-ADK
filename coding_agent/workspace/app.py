
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional

app = FastAPI()

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class Todo(TodoCreate):
    id: int
    completed: bool = False

todos: List[Todo] = []
next_id: int = 1

@app.post("/todos/", response_model=Todo)
def create_todo(todo: TodoCreate):
    global next_id
    new_todo = Todo(id=next_id, title=todo.title, description=todo.description)
    todos.append(new_todo)
    next_id += 1
    return new_todo

@app.get("/todos/", response_model=List[Todo])
def list_todos():
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo_update: TodoCreate):
    for idx, todo in enumerate(todos):
        if todo.id == todo_id:
            updated_todo = todo.copy(update=todo_update.dict(exclude_unset=True))
            todos[idx] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    global todos
    initial_len = len(todos)
    todos = [todo for todo in todos if todo.id != todo_id]
    if len(todos) == initial_len:
        raise HTTPException(status_code=404, detail="Todo not found")
    return
