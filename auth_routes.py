import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.report import ReportPriority, ReportStatus


class ReportCreate(BaseModel):
    reporter_name: str = Field(..., min_length=1, max_length=64)
    reported_player: str = Field(..., min_length=1, max_length=64)
    reason: str = Field(..., min_length=1, max_length=128)
    description: str = Field(..., min_length=1, max_length=2048)
    priority: ReportPriority = ReportPriority.MEDIUM


class ReportUpdate(BaseModel):
    status: Optional[ReportStatus] = None
    priority: Optional[ReportPriority] = None


class ReportResponse(BaseModel):
    id: uuid.UUID
    reporter_name: str
    reported_player: str
    reason: str
    description: str
    priority: ReportPriority
    status: ReportStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ReportFilter(BaseModel):
    status: Optional[ReportStatus] = None
    priority: Optional[ReportPriority] = None
    reported_player: Optional[str] = None


class PaginatedReports(BaseModel):
    items: list[ReportResponse]
    total: int
    page: int
    size: int
    pages: int
