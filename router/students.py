from models import College,Student
from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.orm import Session,Query
import crud.college_crud as college_crud,schemas,database
from crud import student_crud
from typing import Optional
from auth.dependencies import require_roles,get_current_user


students_router = APIRouter(prefix="/students",tags=["students"])

@students_router.post("/students-post/", response_model=schemas.StudentResponse)
def new_student(std: schemas.StudentCreateBase, db: Session = Depends(database.get_db),get_current_user=Depends(require_roles("admin","staff"))):
    return student_crud.create_student(db, std)

@students_router.get("/students-all/",response_model=list[schemas.StudentResponse])
def list_students(skip:int=0,limit:int=10,db:Session=Depends(database.get_db),get_current_user=Depends(require_roles("admin","staff"))):
    return student_crud.retrive_all_students(db,skip=skip,limit=limit)

@students_router.get("/students/{std_id}/",response_model=schemas.StudentResponse,summary="Retrive by student id")
def get_by_id(std_id:int,db:Session=Depends(database.get_db),get_current_user=Depends(require_roles("admin","staff"))):
    return student_crud.retireve_by_id(db,std_id)

@students_router.get("/students-name/",response_model=list[schemas.StudentResponse])
def search_by_name(name:Optional[str] = Query[None],db:Session=Depends(database.get_db),get_current_user=Depends(require_roles("admin","staff"))):
    return student_crud.search_name(db,name)

@students_router.get("/students-college/",response_model=list[schemas.StudentResponse])
def get_by_clg_id(college_id:int,db:Session=Depends(database.get_db),get_current_user=Depends(require_roles("admin","staff"))):
    return student_crud.get_students_by_college(db,college_id)

@students_router.put("/students-update/{std_id}/",response_model=schemas.StudentResponse)
def update_student(std_id:int,student:schemas.StudentCreateBase,db:Session=Depends(database.get_db),get_current_user=Depends(require_roles("admin","staff"))):
    return student_crud.update_student(db,student,std_id)

@students_router.delete("/students-delete/{std_id}/")
def delete_std(std_id:int,db:Session=Depends(database.get_db),get_current_user=Depends(require_roles("admin","staff"))):
    return student_crud.delete_student(db,std_id)

    

