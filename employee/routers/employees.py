from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from database_structure.database import get_db, SessionLocal
from employee.schemas import (
    CreateScheduleRequest,
    UpdateScheduleRequest,
    DeleteScheduleRequest,
)
from employee.services.employees import ScheduleManager

router = APIRouter(prefix="/employee")

ScheduleManagerObj = ScheduleManager()


async def validate_date(date_str: str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {date_str}")


@router.post("/schedule")
async def create_schedule(
    schedule_request: CreateScheduleRequest, db: SessionLocal = Depends(get_db)
):
    return await ScheduleManagerObj.create.create_schedule(
        schedule_request.employee_id,
        schedule_request.full_name,
        schedule_request.day,
        schedule_request.availability,
        db,
    )


@router.get("/schedules")
async def list_schedules(db: SessionLocal = Depends(get_db)):
    return await ScheduleManagerObj.read.list_schedules(db)


@router.get("/schedules/start_date/{start}/end_date/{end}")
async def get_schedules_by_date_range(
    start: str, end: str, db: SessionLocal = Depends(get_db)
):
    start_date = await validate_date(start)
    end_date = await validate_date(end)
    return await ScheduleManagerObj.read.get_schedules_by_date_range(
        start_date, end_date, db
    )


@router.get("/schedules/day/{day}")
async def get_schedules_by_day(day: str, db: SessionLocal = Depends(get_db)):
    return await ScheduleManagerObj.read.get_schedules_by_specific_day(day, db)


@router.get("/schedules/employee/{employee_id}")
async def get_schedules_by_specific_employee(
    employee_id: str, db: SessionLocal = Depends(get_db)
):
    return await ScheduleManagerObj.read.get_schedules_by_employee(employee_id, db)


@router.get("/schedule/employee/{employee_id}/day/{day}")
async def get_schedule_by_specific_employee_and_specific_day(
    employee_id: str, day: str, db: SessionLocal = Depends(get_db)
):
    return await ScheduleManagerObj.read.get_schedule_by_employee_and_specific_day(
        employee_id, day, db
    )


@router.patch("/schedule")
async def update_schedule(
    schedule_request: UpdateScheduleRequest, db: SessionLocal = Depends(get_db)
):
    return await ScheduleManagerObj.update.update_availability(
        schedule_request.employee_id,
        schedule_request.schedule_id,
        schedule_request.new_availability,
        db,
    )


@router.delete("/schedule")
async def delete_schedule(
    schedule_request: DeleteScheduleRequest, db: SessionLocal = Depends(get_db)
):
    return await ScheduleManagerObj.delete.delete_schedule(
        schedule_request.employee_id, schedule_request.schedule_id, db
    )
