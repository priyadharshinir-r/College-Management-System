from database import Base
from sqlalchemy import Column, Integer, ForeignKey, String, Date, DateTime, Text, Enum as SAEnum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime

class College(Base):
    __tablename__ = "colleges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    location = Column(String(100), nullable=True)

    students = relationship("Student", back_populates="college", cascade="all,delete-orphan")
    courses = relationship("Course", back_populates="college", cascade="all,delete-orphan")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    enrollment_no = Column(String(50), unique=True, nullable=False)
    college_id = Column(Integer, ForeignKey("colleges.id", ondelete="CASCADE"))

    college = relationship("College", back_populates="students")

    # Correct placement: Student has many Attendances (reverse side)
    attendances = relationship(
        "Attendance",
        back_populates="student",
        cascade="all,delete-orphan"
    )


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    mode = Column(String(50), nullable=True)
    description = Column(String(400), nullable=True)
    college_id = Column(Integer, ForeignKey("colleges.id", ondelete="CASCADE"))

    college = relationship("College", back_populates="courses")


# ---- User / Role ----
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
    role = Column(SAEnum(RoleEnum), default=RoleEnum.student)

    # one-to-one: User -> Staff (reverse side)
    staff_profile = relationship("Staff", back_populates="user", uselist=False)

    # optional: if you want to access attendances marked by this user (staff)
    # marked_attendances = relationship("Attendance", back_populates="marked_user")


# ---- Attendance ----
class AttendanceStatus(str, enum.Enum):
    present = "present"
    absent = "absent"
    late = "late"
    excused = "excused"


class Attendance(Base):
    __tablename__ = "attendances"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    status = Column(SAEnum(AttendanceStatus), nullable=False)
    marked_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # staff id
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # relationship -> Student (must match Student.attendances)
    student = relationship("Student", back_populates="attendances")

    # simple relationship to the user who marked the attendance
    marked_user = relationship("User")  # optionally add back_populates if you want reverse link


# ---- Staff profile (one-to-one with User) ----
class Staff(Base):
    __tablename__ = "staff_profiles"
    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    employee_no = Column(String(50), unique=True, nullable=False)
    department = Column(String(50), nullable=True)
    designation = Column(String(50), nullable=True)
    joined_at = Column(Date)

    # relationship: Staff.user -> User.staff_profile
    user = relationship("User", back_populates="staff_profile", uselist=False)



