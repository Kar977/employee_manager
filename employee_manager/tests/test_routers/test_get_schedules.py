import pytest

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_get_schedules(mock_db_session_with_schedules):
    response = client.get("/employee/schedules")

    assert response.status_code == 200
    assert "id" in response.json()[0]


@pytest.mark.asyncio
async def test_get_schedules_by_date_range(mock_db_session_with_schedules):
    response = client.get(
        "/employee/schedules/start-date/2025-01-01/end-date/2025-01-02"
    )

    assert response.status_code == 200
    assert "id" in response.json()[0]


@pytest.mark.asyncio
async def test_get_schedules_by_date_range_with_wrong_dates_format(
    mock_db_session_with_schedules,
):
    response = client.get(
        "/employee/schedules/start-date/2025.01.01/end-date/2025.01.02"
    )

    assert response.status_code == 400
    assert "Invalid date format: 2025.01.01" in response.text


@pytest.mark.asyncio
async def test_get_schedules_by_day(mock_db_session_with_schedules):
    response = client.get("/employee/schedules/day/2025-01-02")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_schedules_by_day_with_wrong_date(mock_db_session_with_schedules):
    response = client.get("/employee/schedules/day/2025.01.02")

    assert response.status_code == 400
    assert "Invalid date format: 2025.01.02" in response.text


@pytest.mark.asyncio
async def test_get_schedules_by_employee_id(mock_db_session_with_schedules):
    response = client.get("/employee/schedules/employee/1")

    assert response.status_code == 200
    assert "id" in response.json()[0]


@pytest.mark.asyncio
async def test_get_schedules_by_employee_id_and_specific_date(
    mock_db_session_with_schedule,
):
    response = client.get("/employee/schedule/employee/1/day/2025-01-01")

    assert response.status_code == 200
    assert "2025-01-01" and "Adam Nowak" in response.text


@pytest.mark.asyncio
async def test_get_schedules_by_employee_id_and_wrong_date(
    mock_db_session_with_schedule,
):
    response = client.get("/employee/schedule/employee/1/day/2025.01.01")

    assert response.status_code == 400
    assert "Invalid date format: 2025.01.01" in response.text
