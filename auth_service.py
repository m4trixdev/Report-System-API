import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user, require_admin
from app.repositories.report_repository import ReportRepository
from app.schemas.report_schema import (
    ReportCreate,
    ReportUpdate,
    ReportResponse,
    PaginatedReports,
    ReportFilter,
)
from app.services.report_service import ReportService
from app.models.report import ReportStatus, ReportPriority

router = APIRouter(prefix="/reports", tags=["Reports"])


def get_service(db: AsyncSession = Depends(get_db)) -> ReportService:
    return ReportService(ReportRepository(db))


@router.post("", response_model=ReportResponse, status_code=201)
async def create_report(
    payload: ReportCreate,
    service: ReportService = Depends(get_service),
    _: dict = Depends(get_current_user),
):
    return await service.create(payload)


@router.get("", response_model=PaginatedReports)
async def list_reports(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status: Optional[ReportStatus] = Query(None),
    priority: Optional[ReportPriority] = Query(None),
    reported_player: Optional[str] = Query(None, max_length=64),
    service: ReportService = Depends(get_service),
    _: dict = Depends(get_current_user),
):
    filters = ReportFilter(status=status, priority=priority, reported_player=reported_player)
    return await service.list_reports(page=page, size=size, filters=filters)


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: uuid.UUID,
    service: ReportService = Depends(get_service),
    _: dict = Depends(get_current_user),
):
    return await service.get_by_id(report_id)


@router.patch("/{report_id}", response_model=ReportResponse)
async def update_report(
    report_id: uuid.UUID,
    payload: ReportUpdate,
    service: ReportService = Depends(get_service),
    _: dict = Depends(require_admin),
):
    return await service.update(report_id, payload)


@router.delete("/{report_id}", status_code=204)
async def delete_report(
    report_id: uuid.UUID,
    service: ReportService = Depends(get_service),
    _: dict = Depends(require_admin),
):
    await service.delete(report_id)
