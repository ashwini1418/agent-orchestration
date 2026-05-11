"""Notification schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..models.notification import NotificationType


class NotificationResponse(BaseModel):
    id: str
    user_id: str
    type: NotificationType
    title: str
    message: str
    is_read: bool
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    action_url: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class MarkReadRequest(BaseModel):
    notification_ids: list[str]
