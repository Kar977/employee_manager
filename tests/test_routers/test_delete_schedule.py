import pytest

from fastapi.testclient import TestClient
from employee_manager.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_delete_schedule(mock_db_session_with_schedule):
    response = client.request(
        "DELETE", "/employee/schedule", json={"employee_id": "1", "schedule_id": "1"}
    )

    assert response.status_code == 200
    assert (
        "id"
        and "employee_id"
        and "1"
        and "full_name"
        and "Adam Nowak"
        and "2025-01-01" in response.text
    )


@pytest.mark.asyncio
async def test_delete_schedule_with_not_existing_data(mock_empty_db_session):
    response = client.request(
        "DELETE", "/employee/schedule", json={"employee_id": "1", "schedule_id": "1"}
    )

    assert response.status_code == 404
    assert "resource schedule with ID = 1 does not exist" in response.text
