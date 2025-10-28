from sqlalchemy.orm import Session
from fastapi import status,HTTPException
import database,schemas
from models import College,Student,Attendance
from typing import Optional
from datetime import date
from sqlalchemy import func



def mark_attendance(db: Session, data: schemas.AttendanceCreate, marked_by: int):
    existing = db.query(Attendance).filter(Attendance.student_id == data.student_id, Attendance.date == data.date).first()
    if existing:
        existing.status = data.status
        existing.remarks = data.remarks
        existing.marked_by = marked_by
        db.commit()
        db.refresh(existing)
        return existing
    att = Attendance(**data.dict(), marked_by=marked_by)
    db.add(att)
    db.commit()
    db.refresh(att)
    return att

def bulk_mark_attendance(db: Session, items: list[schemas.AttendanceCreate], marked_by: int):
    results = []
    for item in items:
        results.append(mark_attendance(db, item, marked_by))
    return results

def get_attendance_by_student(db: Session, student_id: int, start: date = None, end: date = None):
    q = db.query(Attendance).filter(Attendance.student_id == student_id)
    if start:
        q = q.filter(Attendance.date >= start)
    if end:
        q = q.filter(Attendance.date <= end)
    return q.order_by(Attendance.date).all()

def attendance_report(db: Session, college_id: int, start: date, end: date):
    return db.query(Attendance.student_id, func.count(Attendance.id).label("present_days")).filter(
        Attendance.date >= start, Attendance.date <= end, Attendance.status == schemas.AttendanceStatus.present
    ).group_by(Attendance.student_id).all()
    