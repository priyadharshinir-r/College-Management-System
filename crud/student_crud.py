from sqlalchemy.orm import Session
from fastapi import status
import crud.college_crud as college_crud,database,schemas
from models import College,Student
from fastapi import status,HTTPException
from typing import Optional



#student crud
def create_student(db: Session, student_in: schemas.StudentCreateBase) -> Student:
    student = Student(
        name=student_in.name,
        email=student_in.email,
        enrollment_no=student_in.enrollment_no,
        college_id=student_in.college_id
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def retrive_all_students(db:Session,skip:int=0,limit:int=10):
    try:
        std = db.query(Student).offset(skip).limit(limit).all()
        return std
    except Exception as e:
        raise HTTPException(status_code=500,detail="id not found")
    
def retireve_by_id(db:Session,std_id:int):
    try:
        std = db.query(Student).filter(Student.id==std_id).first()
        if not std:
            raise HTTPException(status_code=404,detail="id not found")
        return std
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))
    


def search_name(db:Session,name:Optional[str] = None):
    query = db.query(Student) #initialize
    if name:
        query = query.filter(Student.name.ilike(f"%{name}%")) #case senstive
    students = query.all()
    if not students:
        raise HTTPException(status_code=404,detail="There is no location you mentioned")
    return students
    
def get_students_by_college(db:Session,college_id:int):
    clg = db.query(Student).filter(Student.college_id == college_id).all()
    return clg

# def read_student_by_email(db: Session, email: str):
#     return db.query(Student).filter(Student.email == email).first()

def update_student(db:Session,std_id:int,std:schemas.StudentCreateBase):
    try:
        student =db.query(Student).filter(Student.id == std_id).first()
        if not student:
            raise HTTPException(status_code=404,detail=f"{student} id not found")
        
        Student.name=std.name
        Student.email = std.email
        Student.enrollment_no=std.enrollment_no
        Student.college_id=std.college_id
        
        db.add(student)
        db.commit()
        db.refresh(student)
        return student
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))
    
def delete_student(db:Session,std_id:int):
    try:
        student = db.query(Student).filter(Student.id==std_id).first()
        if  not student:
            raise HTTPException(status_code=404,detail=f"{student} is not found")
        db.delete(student)
        db.commit()
        return {"detail": f"{student} id deleted successfull"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))
                