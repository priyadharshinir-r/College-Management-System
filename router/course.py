from models import Course
from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.orm import Session,Query
import schemas,database
from crud import student_crud
from typing import Optional
from crud import course_crud
from auth.dependencies import require_roles,get_current_user


course_router = APIRouter(prefix="/courses",tags=["course"])

@course_router.post("/course-post/",response_model=schemas.CourseResponse)
def new_course(course:schemas.CreateCourse,db:Session=Depends(database.get_db),get_current_user=Depends(require_roles("admin","staff"))):
    return course_crud.create_course(db,course)

@course_router.get("/course-all/",response_model=list[schemas.CourseResponse])
def get_all_courses(db:Session=Depends(database.get_db),get_current_user=Depends(require_roles("admin","student","staff"))):
    return course_crud.get_all_course(db)

@course_router.get("/course-by-id/{course_id}/",response_model=schemas.CourseResponse)
def get_course_by_id(course_id:int,db:Session=Depends(database.get_db),get_current_user=Depends(require_roles("admin","student","staff"))):
    return course_crud.get_courde_by_id(db,course_id)

@course_router.get("/course-by-title/", response_model=list[schemas.CourseResponse])
def search_by_title(
    title: str,
    db: Session = Depends(database.get_db),
    get_current_user = Depends(require_roles("admin", "student", "staff"))
):
    return course_crud.search_course_by_title(db, title)



@course_router.get("/course-by-mode/", response_model=list[schemas.CourseResponse])
def search_by_mode(
    mode: str,
    db: Session = Depends(database.get_db),
    get_current_user = Depends(require_roles("admin", "student", "staff"))
):
    return course_crud.search_course_by_mode(db, mode)



@course_router.put("/update-course/{course_id}/", response_model=schemas.CourseResponse)
def update_course(
    course_id: int,
    course: schemas.CreateCourse,
    db: Session = Depends(database.get_db),
    get_current_user = Depends(require_roles("admin", "staff","student")) 
):
    return course_crud.update_course(db, course_id, course)



@course_router.delete("/delete-course/{course_id}/")
def delete_course(
    course_id: int,
    db: Session = Depends(database.get_db),
    get_current_user = Depends(require_roles("admin", "staff","student"))  
):
    return course_crud.delete_course(db, course_id)
