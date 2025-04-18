from unittest.mock import AsyncMock, MagicMock
import pytest
from employee_manager.database_structure.database import get_db
from employee_manager.database_structure.models import WorkSchedule
from employee_manager.main import app
from datetime import date

mock_session = AsyncMock()


@pytest.fixture(scope="function", autouse=True)
def mocked_app():
    async def override_get_db():
        try:
            yield mock_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db


def mock_work_schedule_obj():
    return WorkSchedule(
        id=1, employee_id=1, full_name="Adam Nowak", day=date(2025, 1, 1)
    )


@pytest.fixture
def mock_db_session_with_schedules():
    mock_result = MagicMock()
    mock_scalars = MagicMock()

    mock_scalars.all.return_value = [mock_work_schedule_obj()]
    mock_result.scalars.return_value = mock_scalars

    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.commit = AsyncMock()
    mock_session.delete = AsyncMock()
    mock_session.add = AsyncMock()

    yield mock_session
    mock_session.reset_mock()


@pytest.fixture
def mock_empty_db_session():
    mock_result = MagicMock()
    mock_scalars = MagicMock()

    mock_scalars.first.return_value = 0
    mock_result.scalars.return_value = mock_scalars

    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.commit = AsyncMock()
    mock_session.delete = MagicMock()
    mock_session.add = MagicMock()

    yield mock_session
    mock_session.reset_mock()


@pytest.fixture
def mock_db_session_with_schedule():
    mock_result = MagicMock()
    mock_scalars = MagicMock()

    mock_scalars.first.return_value = mock_work_schedule_obj()
    mock_result.scalars.return_value = mock_scalars

    mock_session.execute = AsyncMock(return_value=mock_result)
    mock_session.commit = AsyncMock()
    mock_session.delete = AsyncMock()
    mock_session.add = AsyncMock()

    yield mock_session
    mock_session.reset_mock()
