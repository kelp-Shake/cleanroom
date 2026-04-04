from fastapi import APIRouter
from app.db import curr_session as db 
from app.auth import claims, currUser
from app.schemas import UserCreate, UserResponse
from app.services.users import create_user, get_user, update_user


# UserResponse, UserUpdate

user_router = APIRouter()

@user_router.post("/", response_model=UserResponse)
def create_user_router(user: UserCreate, db: db, claims: claims):
    return create_user(db, claims, user)

@user_router.get("/activeUser", response_model= UserResponse)
def get_user_router(user: currUser):
    return get_user(user)

@user_router.patch("/", response_model=UserResponse)
def update_user_router(user: currUser, db: db, create: UserCreate):
    return update_user(db, user, create)