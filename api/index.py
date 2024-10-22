from fastapi import FastAPI
from app.routes import student

app = FastAPI(title="School Management API")

app.include_router(student.router, tags=["students"])
app = app