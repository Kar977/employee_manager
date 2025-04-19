import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from employee_manager.employee.routers.employees import router as employees_router
from employee_manager.database_structure.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


def register_routers():
    app.include_router(employees_router)


register_routers()
