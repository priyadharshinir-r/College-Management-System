# routers/staff_routes.py

from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session
import schemas, crud.staff_crud as staff_crud
from database import get_db
from auth.dependencies import require_roles, get_current_user 
from models import User  

router = APIRouter(prefix="/staff", tags=["Staff"])


@router.post("/", response_model=schemas.StaffResponse, status_code=status.HTTP_201_CREATED)
def create_staff(staff_in: schemas.StaffCreate, db: Session = Depends(get_db),
                 current_user: User = Depends(require_roles("admin"))):
    return staff_crud.create_staff(db, staff_in)


@router.get("/", response_model=List[schemas.StaffResponse])
def list_staff(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
               current_user: User = Depends(require_roles("admin", "staff"))):
    return staff_crud.get_all_staff(db, skip=skip, limit=limit)


@router.get("/{staff_id}/", response_model=schemas.StaffResponse)
def get_staff(staff_id: int, db: Session = Depends(get_db),
              current_user: User = Depends(require_roles("admin", "staff"))):
    return staff_crud.get_staff_by_id(db, staff_id)


@router.put("/{staff_id}/", response_model=schemas.StaffResponse)
def update_staff(staff_id: int, staff_in: schemas.StaffUpdate, db: Session = Depends(get_db),
                 current_user: User = Depends(require_roles("admin"))):
    return staff_crud.update_staff(db, staff_id, staff_in)


@router.delete("/{staff_id}/", status_code=status.HTTP_200_OK)
def delete_staff(staff_id: int, db: Session = Depends(get_db),
                 current_user: User = Depends(require_roles("admin"))):
    return staff_crud.delete_staff(db, staff_id)
