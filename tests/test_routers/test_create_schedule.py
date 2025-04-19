import pytest

from fastapi.testclient import TestClient
from employee_manager.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_schedule(mock_empty_db_session):
    response = client.post(
        "/employee/schedule",
        json={
            "employee_id": "2",
            "full_name": "Adam Sosna",
            "day": "2025-01-02",
            "availability": "07:00-15:00",
        },
    )

    assert response.status_code == 200
    assert "employee_id" and "full_name" and "day" and "availability" in response.json()


@pytest.mark.asyncio
async def test_create_schedule_with_already_existing_schedule(
    mock_db_session_with_schedules,
):
    response = client.post(
        "/employee/schedule",
        json={
            "employee_id": "1",
            "full_name": "Adam Nowak",
            "day": "2025-01-01",
            "availability": "07:00-15:00",
        },
    )

    assert response.status_code == 409
    assert (
        "resource schedule with day & employee = 2025-01-01 00:00:00 & 1 already exist"
        in response.text
    )
