"""Pydantic schemas for API request/response."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TodoCreate(BaseModel):
    """Schema for creating a todo."""

    title: str


class TodoUpdate(BaseModel):
    """Schema for updating a todo (all fields optional)."""

    title: str | None = None
    completed: bool | None = None


class TodoResponse(BaseModel):
    """Schema for todo response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    completed: bool
    created_at: datetime
