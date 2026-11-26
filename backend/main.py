
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

import function


app = FastAPI(title="Campus Connection API")




app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ClubUpdateRequest(BaseModel):
    coordinator_id: int
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None



# A1 - REGISTER

@app.post("/register")
def register(data: function.RegisterCreate):

    result = function.register_user(
        name=data.name,
        email=data.email,
        password=data.password)
    if result is False:
        raise HTTPException(
            status_code=400,
            detail="Email already registered" )
    return {
        "message": "Registration successful",
        "detail": result}



# A2 - LOGIN


@app.post("/login")
def login(data: LoginRequest):

    result = function.login_user(
        email=data.email,
        password=data.password)
    if result is False:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password")

    return {
        "message": "Login successful",
        "detail": result}



# A3 - REFRESH ACCESS TOKEN


@app.post("/refresh")
def refresh_token(data: RefreshTokenRequest):

    result = function.refresh_access_token(
        refresh_token=data.refresh_token
    )

    if result is False:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )

    return {
        "message": "Access token refreshed successfully",
        "detail": result
    }



# E1 - CREATE COORDINATOR


@app.post("/coordinators")
def create_coordinator(data: function.CoordinatorCreate):

    result = function.create_coordinator(
        name=data.name,
        email=data.email,
        password=data.password
    )

    if result is False:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    return {
        "message": "Coordinator created successfully",
        "detail": result
    }

# E2 - CREATE CLUB


@app.post("/clubs")
def create_club(data: function.ClubCreate):

    result = function.create_club(
        name=data.name,
        description=data.description,
        category=data.category,
        coordinator_id=data.coordinator_id
    )

    if result is False:
        raise HTTPException(
            status_code=403,
            detail="Invalid coordinator ID"
        )

    return {
        "message": "Club created successfully",
        "detail": result
    }



# E3 - GET ALL CLUBS


@app.get("/clubs")
def get_clubs():

    result = function.get_clubs()

    return {
        "message": "Clubs fetched successfully",
        "detail": result
    }



# E4 - GET CLUB BY ID

@app.get("/clubs/{club_id}")
def get_club_by_id(club_id: int):

    result = function.get_club_by_id(club_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Club not found"
        )

    return {
        "message": "Club fetched successfully",
        "detail": result
    }
# E5 - UPDATE CLUB

@app.put("/clubs/{club_id}")
def update_club(club_id: int, data: ClubUpdateRequest):

    result = function.update_club(
        club_id=club_id,
        coordinator_id=data.coordinator_id,
        name=data.name,
        description=data.description,
        category=data.category
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Club not found or you are not its coordinator"
        )

    return {
        "message": "Club updated successfully",
        "detail": result
    }
