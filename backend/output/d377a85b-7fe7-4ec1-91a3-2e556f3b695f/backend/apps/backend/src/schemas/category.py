"""Category request/response schemas."""
from typing import Optional

from pydantic import BaseModel, Field, field_validator
import re


class CreateCategoryRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    color: str = Field(default="#6366f1")
    icon: Optional[str] = Field(default=None, max_length=50)
    sort_order: int = Field(default=0, ge=0)

    @field_validator("color")
    @classmethod
    def valid_hex_color(cls, v: str) -> str:
        if not re.match(r"^#[0-9A-Fa-f]{6}$", v):
            raise ValueError("Color must be a valid hex color (e.g., #6366f1)")
        return v.lower()

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be blank")
        return v.strip()


class UpdateCategoryRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    color: Optional[str] = None
    icon: Optional[str] = Field(default=None, max_length=50)
    sort_order: Optional[int] = Field(default=None, ge=0)
    is_default: Optional[bool] = None

    @field_validator("color")
    @classmethod
    def valid_hex_color(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not re.match(r"^#[0-9A-Fa-f]{6}$", v):
            raise ValueError("Color must be a valid hex color (e.g., #6366f1)")
        return v.lower() if v else v


class CategoryResponse(BaseModel):
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    color: str
    icon: Optional[str] = None
    sort_order: int
    is_default: bool
    task_count: int = 0

    model_config = {"from_attributes": True}
