"""AI service request/response schemas."""
from typing import Optional

from pydantic import BaseModel, Field


class AITaskSuggestionRequest(BaseModel):
    context: str = Field(min_length=1, max_length=2000)
    existing_tasks: list[str] = Field(default_factory=list, max_length=20)


class AITaskSuggestion(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str
    estimated_minutes: Optional[int] = None
    tags: list[str] = []


class AITaskSuggestionResponse(BaseModel):
    suggestions: list[AITaskSuggestion]


class NaturalLanguageTaskRequest(BaseModel):
    input: str = Field(min_length=1, max_length=1000)


class NaturalLanguageTaskResponse(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str
    due_date: Optional[str] = None
    estimated_minutes: Optional[int] = None
    tags: list[str] = []
    confidence: float


class AIPriorityRequest(BaseModel):
    task_id: str
    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    context: Optional[str] = None


class AIPriorityResponse(BaseModel):
    suggested_priority: str
    reasoning: str
    confidence: float
