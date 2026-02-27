import math
import uuid
from typing import Optional

from fastapi import HTTPException, status

from app.repositories.report_repository import ReportRepository
from app.schemas.report_schema import (
    ReportCreate,
    ReportUpdate,
    ReportResponse,
    PaginatedReports,
    ReportFilter,
)
from app.models.report import ReportStatus, ReportPriority
from app.core.logging import get_logger

logger = get_logger(__name__)


class ReportService:
    def __init__(self, repo: ReportRepository):
        self.repo = repo

    async def create(self, payload: ReportCreate) -> ReportResponse:
        report = await self.repo.create(payload.model_dump())
        logger.info("report_created", id=str(report.id), reported=report.reported_player)
        return ReportResponse.model_validate(report)

    async def get_by_id(self, report_id: uuid.UUID) -> ReportResponse:
        report = await self.repo.get_by_id(report_id)
        if not report:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
        return ReportResponse.model_validate(report)

    async def list_reports(
        self,
        page: int,
        size: int,
        filters: ReportFilter,
    ) -> PaginatedReports:
        if page < 1:
            page = 1
        if size < 1 or size > 100:
            size = 20

        items, total = await self.repo.get_paginated(
            page=page,
            size=size,
            status=filters.status,
            priority=filters.priority,
            reported_player=filters.reported_player,
        )

        return PaginatedReports(
            items=[ReportResponse.model_validate(r) for r in items],
            total=total,
            page=page,
            size=size,
            pages=max(1, math.ceil(total / size)),
        )

    async def update(self, report_id: uuid.UUID, payload: ReportUpdate) -> ReportResponse:
        existing = await self.repo.get_by_id(report_id)
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")

        update_data = payload.model_dump(exclude_none=True)
        if not update_data:
            return ReportResponse.model_validate(existing)

        updated = await self.repo.update(report_id, update_data)
        logger.info("report_updated", id=str(report_id), changes=update_data)
        return ReportResponse.model_validate(updated)

    async def delete(self, report_id: uuid.UUID) -> None:
        existing = await self.repo.get_by_id(report_id)
        if not existing:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
        await self.repo.delete(report_id)
        logger.info("report_deleted", id=str(report_id))
