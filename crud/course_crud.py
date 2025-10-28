from sqlalchemy.orm import Session
from fastapi import status
import database,schemas
from models import Course
from fastapi import status,HTTPException
from typing import Optional


def create_course(db:Session,course:schemas.CreateCourse):
    try:
        new_course = Course(
            title = course.title,
            mode = course.mode,
            description = course.description,
            college_id = course.college_id
        )
        db.add(new_course)
        db.commit()
        db.refresh(new_course)
        return new_course
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))
    

def get_all_course(db:Session):
    course = db.query(Course).all()
    return course

def get_courde_by_id(db:Session,course_id:int):
    try:
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404,detail=f"{course} not found")
        return course
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))
    
    
def search_course_by_title(db: Session, title: str):
    query = db.query(Course)
    if title:
        query = query.filter(Course.title.ilike(f"%{title}%"))
    courses = query.all()
    if not courses:
        raise HTTPException(status_code=404, detail="No course with that title found")
    return courses


def search_course_by_mode(db: Session, mode: str):
    query = db.query(Course)
    if mode:
        query = query.filter(Course.mode.ilike(f"%{mode}%"))
    courses = query.all()
    if not courses:
        raise HTTPException(status_code=404, detail="No course with that mode found")
    return courses


def update_course(db: Session, course_id: int, course: schemas.CreateCourse):
    try:
        db_course = db.query(Course).filter(Course.id == course_id).first()
        if not db_course:
            raise HTTPException(status_code=404, detail=f"Course ID {course_id} not found")

        db_course.title = course.title
        db_course.mode = course.mode
        db_course.description = course.description
        db_course.college_id = course.college_id

        db.commit()
        db.refresh(db_course)
        return db_course

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


def delete_course(db: Session, course_id: int):
    try:
        course = db.query(Course).filter(Course.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail=f"Course ID {course_id} not found")

        db.delete(course)
        db.commit()
        return {"detail": "Course deleted successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))