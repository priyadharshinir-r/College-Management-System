from models import College,Student
from fastapi import APIRouter,status,HTTPException,Depends,Query
from sqlalchemy.orm import Session
import schemas,database
from crud import attendance_crud
from typing import Optional
from auth.dependencies import get_current_user,require_roles
from datetime import  date
from models import User

attendance_router = APIRouter(prefix="/colleges",tags=["Attendance"])

@attendance_router.post("/mark/", response_model=schemas.AttendanceResponse)
def mark_attendance_route(item: schemas.AttendanceCreate, db: Session = Depends(database.get_db), current_user: User = Depends(require_roles("staff", "admin"))):
    return attendance_crud.mark_attendance(db, item, marked_by=current_user.id)

@attendance_router.post("/mark/bulk/", response_model=list[schemas.AttendanceResponse])
def bulk_mark_route(items: list[schemas.AttendanceCreate], db: Session = Depends(database.get_db), current_user: User = Depends(require_roles("staff", "admin"))):
    return attendance_crud.bulk_mark_attendance(db, items, marked_by=current_user.id)

@attendance_router.get("/student/{student_id}/", response_model=list[schemas.AttendanceResponse])
def get_student_attendance(student_id: int, start: Optional[date]=None, end: Optional[date]=None, db: Session = Depends(database.get_db), current_user: User = Depends(require_roles("staff","admin","student"))):
    return attendance_crud.get_attendance_by_student(db, student_id, start, end)
