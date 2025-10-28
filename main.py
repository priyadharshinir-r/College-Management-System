from fastapi import FastAPI
from models import College ,Student
import schemas,database
from router import college,students,course
from database import Base,get_db,engine
from auth import routes as auth_routes

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)
app.include_router(college.college_router)
app.include_router(students.students_router)
app.include_router(course.course_router)

