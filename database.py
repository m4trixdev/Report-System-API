import uuid
import math
from typing import Optional

from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.report import Report, ReportStatus, ReportPriority


class ReportRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> Report:
        report = Report(**data)
        self.db.add(report)
        await self.db.commit()
        await self.db.refresh(report)
        return report

    async def get_by_id(self, report_id: uuid.UUID) -> Optional[Report]:
        result = await self.db.execute(select(Report).where(Report.id == report_id))
        return result.scalar_one_or_none()

    async def get_paginated(
        self,
        page: int,
        size: int,
        status: Optional[ReportStatus] = None,
        priority: Optional[ReportPriority] = None,
        reported_player: Optional[str] = None,
    ) -> tuple[list[Report], int]:
        query = select(Report)
        count_query = select(func.count()).select_from(Report)

        if status:
            query = query.where(Report.status == status)
            count_query = count_query.where(Report.status == status)
        if priority:
            query = query.where(Report.priority == priority)
            count_query = count_query.where(Report.priority == priority)
        if reported_player:
            query = query.where(Report.reported_player.ilike(f"%{reported_player}%"))
            count_query = count_query.where(Report.reported_player.ilike(f"%{reported_player}%"))

        total_result = await self.db.execute(count_query)
        total = total_result.scalar_one()

        offset = (page - 1) * size
        query = query.order_by(Report.created_at.desc()).offset(offset).limit(size)

        result = await self.db.execute(query)
        items = result.scalars().all()

        return list(items), total

    async def update(self, report_id: uuid.UUID, data: dict) -> Optional[Report]:
        await self.db.execute(
            update(Report).where(Report.id == report_id).values(**data)
        )
        await self.db.commit()
        return await self.get_by_id(report_id)

    async def delete(self, report_id: uuid.UUID) -> bool:
        result = await self.db.execute(
            delete(Report).where(Report.id == report_id)
        )
        await self.db.commit()
        return result.rowcount > 0
