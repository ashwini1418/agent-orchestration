"""Analytics response schemas."""
from typing import Optional

from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_tasks: int
    completed_tasks: int
    overdue_tasks: int
    in_progress_tasks: int
    completion_rate: float
    current_streak: int
    longest_streak: int
    tasks_due_today: int


class CompletionDataPoint(BaseModel):
    date: str
    completed: int
    created: int


class CategoryBreakdown(BaseModel):
    category_id: Optional[str] = None
    category_name: str
    color: str
    count: int
    percentage: float


class PriorityBreakdown(BaseModel):
    priority: str
    count: int
    percentage: float


class ProductivityHeatmapPoint(BaseModel):
    date: str
    count: int
    level: int  # 0-4 for GitHub-style heatmap


class AnalyticsDashboardResponse(BaseModel):
    stats: DashboardStats
    completion_trend: list[CompletionDataPoint]
    category_breakdown: list[CategoryBreakdown]
    priority_breakdown: list[PriorityBreakdown]
    productivity_heatmap: list[ProductivityHeatmapPoint]


class TagResponse(BaseModel):
    id: str
    name: str
    color: str
    task_count: int = 0

    model_config = {"from_attributes": True}
