from pydantic import BaseModel
from typing import List, Optional
from enum import Enum as PyEnum


class CollegeCreate(BaseModel):
    name: str
    location: Optional[str] = None

class CollegeUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None

class CollegeResponse(BaseModel):
    id: int
    name: str
    location: Optional[str]

    class Config:
        from_attributes = True

class CreateCourse(BaseModel):
    title: str
    mode: Optional[str] = None
    description: Optional[str] = None
    college_id: int

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    mode: Optional[str] = None
    description: Optional[str] = None
    college_id: Optional[int] = None


class CourseResponse(BaseModel):
    id: int
    title: str
    mode: Optional[str]
    description: Optional[str]
    college_id: int
    college: Optional[CollegeResponse] = None 

    class Config:
        from_attributes = True




class StudentCreateBase(BaseModel):
    name: Optional[str] = None
    email: str
    enrollment_no: str
    college_id: int

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    college_id: Optional[int] = None

class StudentResponse(BaseModel):
    id: int
    name: Optional[str]
    email: str
    enrollment_no: str
    college_id: int
    college: Optional[CollegeResponse] = None  

    class Config:
        from_attributes = True
        
        
class RoleEnum(str,PyEnum):
    admin = "admin"
    staff = "staff"
    student = "student"
    
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[RoleEnum] = None
    
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: RoleEnum




# CourseResponse.update_forward_refs()
# CollegeResponse.update_forward_refs()