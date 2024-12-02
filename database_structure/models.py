from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, validates

from database_structure.database import db_engine

Base = declarative_base()

VALID_HOURS_RANGE = (
    "07:00-15:00",
    "08:00-16:00",
    "09:00-17:00",
    "10:00-18:00",
    "Day Off",
)


class WorkSchedule(Base):

    __tablename__ = "workschedule"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    employee_id = Column("employee_id", String, nullable=False)
    full_name = Column("full_name", String, nullable=False)
    day = Column("day", Date, nullable=False)
    availability = Column(
        "availability", String, nullable=False, default=VALID_HOURS_RANGE[-1]
    )

    @validates("availability")
    def validate_availability(self, key, availability):
        if availability not in VALID_HOURS_RANGE:
            raise ValueError(
                f"Invalid availability range - {availability}. Must be one of {VALID_HOURS_RANGE}"
            )
        return availability


Base.metadata.create_all(bind=db_engine)
