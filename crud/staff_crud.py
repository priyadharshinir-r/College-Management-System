from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import Staff, User  
import schemas

def create_staff(db: Session, staff_in: schemas.StaffCreate):
    user = db.query(User).filter(User.id == staff_in.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    try:
        # set user role to staff if different
        if getattr(user, "role", None) != "staff":
            user.role = "staff"
            db.add(user)

        # ensure employee_no unique
        existing = db.query(Staff).filter(Staff.employee_no == staff_in.employee_no).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="employee_no already exists")

        staff = Staff(
            id=staff_in.user_id,  # primary key is FK to users.id — matches your model
            employee_no=staff_in.employee_no,
            department=staff_in.department,
            designation=staff_in.designation,
            joined_at=staff_in.joined_at
        )
        db.add(staff)
        db.commit()
        db.refresh(staff)
        return staff
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def get_staff_by_id(db: Session, staff_id: int):
    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    return staff


def get_all_staff(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Staff).offset(skip).limit(limit).all()


def update_staff(db: Session, staff_id: int, staff_in: schemas.StaffUpdate):
    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    try:
        data = staff_in.dict(exclude_unset=True)
        for field, value in data.items():
            setattr(staff, field, value)
        db.add(staff)
        db.commit()
        db.refresh(staff)
        return staff
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def delete_staff(db: Session, staff_id: int):
    staff = db.query(Staff).filter(Staff.id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    try:
        db.delete(staff)
        user = db.query(User).filter(User.id == staff_id).first()
        if user:
            db.add(user)
        db.commit()
        return {"detail": "Staff deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
