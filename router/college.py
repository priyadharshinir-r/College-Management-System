from models import College,Student
from fastapi import APIRouter,status,HTTPException,Depends,Query
from sqlalchemy.orm import Session
import schemas,database
from crud import college_crud
from typing import Optional
from auth.dependencies import require_roles,get_current_user

college_router = APIRouter(prefix="/colleges",tags=["colleges"])

@college_router.post("/college-post/",response_model = schemas.CollegeResponse)
def new_clg(clg:schemas.CollegeCreate,db:Session=Depends(database.get_db),get_current_user=Depends(require_roles("admin","staff"))):
    return college_crud.create_college(db,clg)

@college_router.get("/get-all-colleges/",response_model=list[schemas.CollegeResponse])
def list_college(skip:int=0,limit:int=10,db:Session=Depends(database.get_db),get_current_user=Depends(require_roles("admin","staff"))):
    return college_crud.retrive_all_colleges(db,skip=skip,limit=limit)

@college_router.get("/get-all-by-id/{clg_id}/",response_model=schemas.CollegeResponse)
def list_college_by_id(clg_id:int,db:Session=Depends(database.get_db),get_current_user=Depends(require_roles("admin","staff"))):
    return college_crud.retrieve_college_by_id(db,clg_id)

@college_router.get("/Search-by-location/",response_model =list[schemas.CollegeResponse])
def search_location(
                    location:Optional[str] = Query(None),
                    skip:int=Query(0,ge=0),
                    limit:int=Query(10,ge=1),
                    db:Session=Depends(database.get_db),
                    get_current_user=Depends(require_roles("admin","staff"))
                    ):
    return college_crud.search_by_location(db,location,skip,limit)

@college_router.put("/college-update/{college_id}/",response_model=schemas.CollegeResponse)
def update_update(clg:schemas.CollegeCreate,college_id:int,db:Session=Depends(database.get_db),get_current_user=Depends(require_roles("admin","staff"))):
    return college_crud.update_college(db,college_id,clg)

@college_router.patch("/college-patch/{college_id}/",response_model=schemas.CollegeResponse)
def partial_update(clg:schemas.CollegeUpdate,college_id:int,db:Session=Depends(database.get_db),get_current_user=Depends(require_roles("admin","staff"))):
    return college_crud.partial_update_college(db,college_id,clg)


@college_router.delete("/college-delete/{college_id}/")
def delete_college_by_id(college_id:int,db:Session=Depends(database.get_db),get_current_user=Depends(require_roles("admin","staff"))):
    return college_crud.delete_college(db,college_id)
