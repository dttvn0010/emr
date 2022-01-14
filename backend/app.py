from fastapi import FastAPI

from components.user.views import router as user_router
from components.department.views import router as department_router

app = FastAPI()

app.include_router(user_router)
app.include_router(department_router)