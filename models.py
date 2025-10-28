from database import Base
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
import enum

class College(Base):
    __tablename__ = "colleges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    location = Column(String(100), nullable=True)

    # Relationships
    students = relationship("Student", back_populates="college", cascade="all,delete-orphan")
    courses = relationship("Course", back_populates="college", cascade="all,delete-orphan")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    enrollment_no = Column(String(50), unique=True, nullable=False)
    college_id = Column(Integer, ForeignKey("colleges.id", ondelete="CASCADE"))

    # Relationship
    college = relationship("College", back_populates="students")


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    mode = Column(String(50), nullable=True)
    description = Column(String(400), nullable=True)
    college_id = Column(Integer, ForeignKey("colleges.id", ondelete="CASCADE"))

    # Relationship
    college = relationship("College", back_populates="courses")


from sqlalchemy import Column, Integer, String, Enum
from database import Base
import enum

#Define Enum (only role values)
class RoleEnum(str, enum.Enum):
    admin = "admin"
    staff = "staff"
    student = "student"



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(500))
    email = Column(String(100), unique=True, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.student) 
