"""Todos CRUD endpoints."""

from fastapi import APIRouter, HTTPException

from app.database import get_session
from app.models import Todo
from app.schemas import TodoCreate, TodoResponse, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", response_model=list[TodoResponse])
def list_todos() -> list[TodoResponse]:
    """List all todos."""
    with get_session() as session:
        todos = list(session.query(Todo).all())
        return [TodoResponse.model_validate(t) for t in todos]


@router.post("", response_model=TodoResponse, status_code=201)
def create_todo(body: TodoCreate) -> TodoResponse:
    """Create a todo."""
    with get_session() as session:
        todo = Todo(title=body.title)
        session.add(todo)
        session.flush()
        session.refresh(todo)
        return TodoResponse.model_validate(todo)


@router.patch("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, body: TodoUpdate) -> TodoResponse:
    """Update a todo by id."""
    with get_session() as session:
        todo = session.get(Todo, todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        if body.title is not None:
            todo.title = body.title
        if body.completed is not None:
            todo.completed = body.completed
        session.flush()
        session.refresh(todo)
        return TodoResponse.model_validate(todo)


@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int) -> None:
    """Delete a todo by id."""
    with get_session() as session:
        todo = session.get(Todo, todo_id)
        if todo is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        session.delete(todo)
        return None
