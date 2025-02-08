from http.client import HTTPException

from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database_structure.models import WorkSchedule
from employee.services.exceptions import (
    ResourceDoesNotExistException,
    ResourceAlreadyExistException,
)


class ScheduleManager:
    def __init__(self):
        self.create = CreateSchedule()
        self.read = ReadSchedule()
        self.update = UpdateSchedule()
        self.delete = DeleteSchedule()


class CreateSchedule:
    async def create_schedule(
        self,
        employee_id: str,
        full_name: str,
        day: str,
        availability: str,
        db: AsyncSession,
    ):

        stmt = select(WorkSchedule).where(
            (WorkSchedule.employee_id == employee_id) & (WorkSchedule.day == day)
        )
        instance = await db.execute(stmt)

        if instance.scalars().first():
            raise ResourceAlreadyExistException(
                resource_name="schedule",
                unit="day & employee",
                identification_mark=f"{day} & {employee_id}",
            )

        new_schedule = WorkSchedule(
            employee_id=employee_id,
            full_name=full_name,
            day=day,
            availability=availability,
        )
        try:
            db.add(new_schedule)
            await db.commit()
            await db.refresh(new_schedule)
        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error occurred while creating schedule: {str(e)}",
            )
        return new_schedule


class ReadSchedule:
    async def list_schedules(self, db: AsyncSession):
        stmt = select(WorkSchedule)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_schedules_by_date_range(self, start: str, end: str, db: AsyncSession):
        stmt = select(WorkSchedule).where(WorkSchedule.day.between(start, end))
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_schedules_by_specific_day(self, day, db: AsyncSession):
        stmt = select(WorkSchedule).where(WorkSchedule.day == day)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_schedules_by_employee(self, employee_id, db: AsyncSession):
        stmt = select(WorkSchedule).where(WorkSchedule.employee_id == employee_id)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_schedule_by_employee_and_specific_day(
        self, employee_id, day, db: AsyncSession
    ):
        stmt = select(WorkSchedule).where(
            and_(WorkSchedule.employee_id == employee_id, WorkSchedule.day == day)
        )
        result = await db.execute(stmt)
        return result.scalars().first()


class UpdateSchedule:
    async def update_availability(
        self,
        employee_id: str,
        schedule_id: int,
        new_availability: str,
        db: AsyncSession,
    ):
        stmt = select(WorkSchedule).where(
            (WorkSchedule.employee_id == employee_id) & (WorkSchedule.id == schedule_id)
        )

        result = await db.execute(stmt)
        schedule = result.scalars().first()
        if not schedule:
            raise ResourceDoesNotExistException(
                resource_name="schedule",
                unit="ID",
                identification_mark=str(schedule_id),
            )

        schedule.availability = new_availability
        await db.commit()
        await db.refresh(schedule)

        return schedule


class DeleteSchedule:
    async def delete_schedule(
        self, employee_id: str, schedule_id: int, db: AsyncSession
    ):

        stmt = select(WorkSchedule).where(
            (WorkSchedule.employee_id == employee_id) & (WorkSchedule.id == schedule_id)
        )
        result = await db.execute(stmt)
        schedule = result.scalars().first()

        if not schedule:
            raise ResourceDoesNotExistException(
                resource_name="schedule",
                unit="ID",
                identification_mark=str(schedule_id),
            )
        await db.delete(schedule)
        await db.commit()

        return schedule
