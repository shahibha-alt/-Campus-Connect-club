
from sqlalchemy import (Integer, String, Column, create_engine, DateTime, ForeignKey, Boolean)
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from pydantic import BaseModel, Field
from typing import Optional

ph = PasswordHasher()

DB_PATH = "campus.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
USERNAME = "shahibha"
PASSWORD = "123456789" 
SECRET_KEY = "sha123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="student")


class Clubs(Base):
    __tablename__ = "clubs"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    category = Column(String)
    coordinator_id = Column(Integer, ForeignKey("users.id"))


class ClubMemberships(Base):
    __tablename__ = "club_memberships"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    club_id = Column(Integer, ForeignKey("clubs.id"))
    status = Column(String, default="pending")
    requested_at = Column(DateTime, default=datetime.now)

    


class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    club_id = Column(Integer, ForeignKey("clubs.id"))
    title = Column(String)
    description = Column(String)
    venue = Column(String)
    event_date = Column(DateTime)
    max_participants = Column(Integer)
    registration_deadline = Column(DateTime)


class EventRegistrations(Base):
    __tablename__ = "event_registrations"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    registered_at = Column(DateTime, default=datetime.now)
    status = Column(String, default="registered")
    attended = Column(Boolean, default=False)


class RegisterCreate(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class CoordinatorCreate(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class ClubCreate(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    category: str = Field(min_length=1)
    coordinator_id: int


class ClubUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None


class MembershipDecision(BaseModel):
    status: str


class EventCreate(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    venue: str = Field(min_length=1)
    event_date: datetime
    max_participants: int = Field(gt=0)
    registration_deadline: datetime


class AttendanceUpdate(BaseModel):
    student_id: int
    attended: bool = True




def user_to_dict(user):
    return {  
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }


def club_to_dict(club):
    return {
        "id": club.id,
        "name": club.name,
        "description": club.description,
        "category": club.category,
        "coordinator_id": club.coordinator_id
    }


def event_to_dict(event):
    return {
        "id": event.id,
        "club_id": event.club_id,
        "title": event.title,
        "description": event.description,
        "venue": event.venue,
        "event_date": event.event_date,
        "max_participants": event.max_participants,
        "registration_deadline": event.registration_deadline,
    }


def registration_to_dict(registration):
    return {
        "id": registration.id,
        "event_id": registration.event_id,
        "student_id": registration.student_id,
        "registered_at": registration.registered_at,
        "status": registration.status,
        "attended": registration.attended,
    }



# PASSWORD FUNCTIONS


def hash_password(password):
    return ph.hash(password)


def verify_password(password, hashed_password):
    try:
        ph.verify(hashed_password, password)
        return True
    except (VerifyMismatchError, InvalidHashError):
        return False


# A1 - REGISTER


def register_user(name, email, password):
    session = Session(engine)
    existing_user = session.query(Users).filter_by(email=email).first()
    if existing_user is not None:
        session.close()
        return False
    hashed_password = ph.hash(password)
    new_user = Users(name=name, email=email,password=hashed_password,role="student")
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    response = user_to_dict(new_user)
    session.close()
    return response




