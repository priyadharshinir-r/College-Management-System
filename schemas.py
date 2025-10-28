from pydantic import BaseModel,Field
from typing import List, Optional
from enum import Enum as PyEnum
from datetime import date
from models import AttendanceStatus




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
    
class AttendanceCreate(BaseModel):
    student_id: int
    date: date
    status: AttendanceStatus
    remarks: Optional[str] = None
    
class AttendanceResponse(BaseModel):
    id: int
    student_id: int
    date: date
    status: AttendanceStatus
    marked_by: Optional[int]
    remarks: Optional[str]

    class Config:
        from_attributes = True

class StaffCreate(BaseModel):
    employee_no: str
    department: Optional[str] = None
    designation: Optional[str] = None
    joined_at: Optional[date] = None
    user_id: int  

class StaffUpdate(BaseModel):
    employee_no: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    joined_at: Optional[date] = None


class StaffResponse(BaseModel):
    id: int
    employee_no: str
    department: Optional[str] = None
    designation: Optional[str] = None
    joined_at: Optional[date] = None

    class Config:
        from_attributes = True



# CourseResponse.update_forward_refs()
# CollegeResponse.update_forward_refs()