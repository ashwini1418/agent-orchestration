"""Task request/response schemas with full Pydantic validation."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from ..models.task import Priority, TaskStatus


class TagResponse(BaseModel):
    id: str
    name: str
    color: str

    model_config = {"from_attributes": True}


class SubTaskResponse(BaseModel):
    id: str
    title: str
    is_completed: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class AttachmentResponse(BaseModel):
    id: str
    filename: str
    file_url: str
    mime_type: str
    file_size: int
    created_at: datetime

    model_config = {"from_attributes": True}


class CommentResponse(BaseModel):
    id: str
    user_id: str
    content: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskResponse(BaseModel):
    id: str
    user_id: str
    category_id: Optional[str] = None
    parent_task_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    priority: Priority
    status: TaskStatus
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    estimated_minutes: Optional[int] = None
    sort_order: float
    reminder_at: Optional[datetime] = None
    recurrence_rule: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    tags: list[TagResponse] = []
    subtasks: list[SubTaskResponse] = []
    attachments: list[AttachmentResponse] = []

    model_config = {"from_attributes": True}

    @classmethod
    def from_orm_with_tags(cls, task: object) -> "TaskResponse":
        """Flatten TaskTag → Tag relationship."""
        data = {
            "id": task.id,
            "user_id": task.user_id,
            "category_id": task.category_id,
            "parent_task_id": task.parent_task_id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "status": task.status,
            "due_date": task.due_date,
            "completed_at": task.completed_at,
            "estimated_minutes": task.estimated_minutes,
            "sort_order": task.sort_order,
            "reminder_at": task.reminder_at,
            "recurrence_rule": task.recurrence_rule,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "tags": [
                TagResponse(id=tt.tag.id, name=tt.tag.name, color=tt.tag.color)
                for tt in task.tags
                if tt.tag
            ],
            "subtasks": [
                SubTaskResponse.model_validate(st)
                for st in task.subtasks
                if not st.is_deleted
            ],
            "attachments": [
                AttachmentResponse.model_validate(a) for a in task.attachments
            ],
        }
        return cls(**data)


class CreateTaskRequest(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=10000)
    priority: Priority = Priority.NONE
    status: TaskStatus = TaskStatus.TODO
    due_date: Optional[datetime] = None
    category_id: Optional[str] = None
    tag_ids: list[str] = Field(default_factory=list, max_length=20)
    estimated_minutes: Optional[int] = Field(default=None, ge=1, le=10080)
    parent_task_id: Optional[str] = None
    reminder_at: Optional[datetime] = None
    recurrence_rule: Optional[str] = Field(default=None, max_length=255)

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be blank")
        return v.strip()


class UpdateTaskRequest(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    description: Optional[str] = Field(default=None, max_length=10000)
    priority: Optional[Priority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    category_id: Optional[str] = None
    tag_ids: Optional[list[str]] = Field(default=None, max_length=20)
    estimated_minutes: Optional[int] = Field(default=None, ge=1, le=10080)
    parent_task_id: Optional[str] = None
    reminder_at: Optional[datetime] = None
    recurrence_rule: Optional[str] = Field(default=None, max_length=255)
    sort_order: Optional[float] = None

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("Title cannot be blank")
        return v.strip() if v else v


class TaskFilterParams(BaseModel):
    status: Optional[TaskStatus] = None
    priority: Optional[Priority] = None
    category_id: Optional[str] = None
    tag_id: Optional[str] = None
    due_before: Optional[datetime] = None
    due_after: Optional[datetime] = None
    search: Optional[str] = Field(default=None, max_length=255)
    is_overdue: Optional[bool] = None
    parent_task_id: Optional[str] = None
    cursor: Optional[str] = None
    limit: int = Field(default=20, ge=1, le=100)
    sort_by: str = Field(default="created_at")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")


class CreateSubTaskRequest(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    sort_order: int = 0


class UpdateSubTaskRequest(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=500)
    is_completed: Optional[bool] = None
    sort_order: Optional[int] = None


class CreateCommentRequest(BaseModel):
    content: str = Field(min_length=1, max_length=5000)


class BulkUpdateRequest(BaseModel):
    task_ids: list[str] = Field(min_length=1, max_length=100)
    status: Optional[TaskStatus] = None
    priority: Optional[Priority] = None
    category_id: Optional[str] = None


class ReorderTasksRequest(BaseModel):
    task_orders: list[dict] = Field(min_length=1)  # [{"id": str, "sort_order": float}]
