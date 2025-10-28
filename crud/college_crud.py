from sqlalchemy.orm import Session
from fastapi import status,HTTPException
import database,schemas
from models import College,Student
from typing import Optional


#college crud
def create_college(db:Session,clg:schemas.CollegeCreate):
    try:
        new_college = College(
            name = clg.name,
            location = clg.location
        )
        db.add(new_college)
        db.commit()
        db.refresh(new_college)
        return new_college
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))
    
def retrive_all_colleges(db:Session,skip:int=0,limit:int=10):
    try:
        clg = db.query(College).offset(skip).limit(limit).all()
        return clg
    except Exception as e :
        raise HTTPException(status_code=500,detail=str(e))
    
    
def retrieve_college_by_id(db:Session,clg_id:int):
    try:
        clg = db.query(College).filter(College.id==clg_id).first()
        if not clg:
            raise HTTPException(status_code=404,detail=f"clg {clg} not found")
        return clg
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))
    
def search_by_location(db:Session,location:Optional[str]=None,skip:int=0,limit:int=10):
        query=db.query(College)
        if location:
            query = query.filter(College.location.ilike(f"%{location}%"))
        colleges = query.offset(skip).limit(limit).all()
        if not colleges:
            raise HTTPException(status_code=404,detail="There is no location you mentioned")
        return colleges
    
    
def update_college(db:Session,college_id:int,clg:schemas.CollegeCreate):
    try:
        college = db.query(College).filter(College.id == college_id).first()
        if not college:
            raise HTTPException(status_code=404,detail=F"mentioned college {college} not found")
        
        College.name = clg.name
        College.location = clg.name
            
        db.add(college)
        db.commit()
        db.refresh(college)
        return college
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))
    
    
def partial_update_college(db:Session,college_id:int,clg:schemas.CollegeUpdate):
    try:
        college = db.query(College).filter(College.id == college_id).first()
        if not college:
            raise HTTPException(status_code=404,detail="Id not found")
        
        if clg.name is not None:
            college.name = clg.name
        if clg.location is not None:
            college.location = clg.location
            
        db.commit()
        db.refresh(college)
        return college

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))
    
def delete_college(db:Session,college_id:int):
    try:
        clg = db.query(College).filter(College.id == college_id).first()
        if not clg:
            raise HTTPException(status_code=404,detail="Id not found")
        
        db.delete(clg)
        db.commit()
        return {"detail": f"College {college_id} deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=str(e))
        
            