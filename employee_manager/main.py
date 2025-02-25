from fastapi import FastAPI

from employee.routers.employees import router as employees_router

app = FastAPI()


def register_routers():
    app.include_router(employees_router)


register_routers()
