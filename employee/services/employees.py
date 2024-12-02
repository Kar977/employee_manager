from http.client import HTTPException

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
        self, employee_id: str, full_name: str, day: str, availability: str, db
    ):
        instance = (
            db.query(WorkSchedule).filter_by(employee_id=employee_id, day=day).first()
        )

        if instance:
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
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error occurred while creating schedule: {str(e)}",
            )
        return new_schedule


class ReadSchedule:
    async def list_schedules(self, db):
        return db.query(WorkSchedule).all()

    async def get_schedules_by_date_range(self, start: str, end: str, db):
        return (
            db.query(WorkSchedule)
            .filter(WorkSchedule.day >= start, WorkSchedule.day <= end)
            .all()
        )

    async def get_schedules_by_specific_day(self, day, db):
        return db.query(WorkSchedule).filter(WorkSchedule.day == day).all()

    async def get_schedules_by_employee(self, employee_id, db):
        return (
            db.query(WorkSchedule).filter(WorkSchedule.employee_id == employee_id).all()
        )

    async def get_schedule_by_employee_and_specific_day(self, employee_id, day, db):
        return (
            db.query(WorkSchedule)
            .filter(WorkSchedule.employee_id == employee_id, WorkSchedule.day == day)
            .first()
        )


class UpdateSchedule:
    async def update_availability(
        self, employee_id: str, schedule_id: int, new_availability: str, db
    ):
        schedule = (
            db.query(WorkSchedule)
            .filter_by(employee_id=employee_id, id=schedule_id)
            .first()
        )

        if not schedule:
            raise ResourceDoesNotExistException(
                resource_name="schedule",
                unit="ID",
                identification_mark=str(schedule_id),
            )

        schedule.availability = new_availability
        db.commit()

        return schedule


class DeleteSchedule:
    async def delete_schedule(self, employee_id: str, schedule_id: int, db):
        schedule = (
            db.query(WorkSchedule)
            .filter_by(employee_id=employee_id, id=schedule_id)
            .first()
        )

        if not schedule:
            raise ResourceDoesNotExistException(
                resource_name="schedule",
                unit="ID",
                identification_mark=str(schedule_id),
            )
        db.delete(schedule)
        db.commit()

        return schedule
