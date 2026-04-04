from fastapi import APIRouter
from app.db import curr_session as db
from auth import currUser
from app.models import User, Area
from app.schemas import UserResponse, AreaCreate, AreaResponse
from app.services.areas import create_area, get_area, get_user_areas, get_area_user_members, get_user_areauser, get_area_user, add_area_users, remove_area_users, delete_area

area_router = APIRouter()

@area_router.post("/", response_model=AreaResponse)
def add_area_router(db: db, currUser: currUser, newArea: AreaCreate):
    return create_area(db, currUser, newArea.name)

@area_router.get("/{area_id}", response_model=AreaResponse)
def get_area_router(db: db,currUser: currUser, area_id:int):
    return get_area(db, currUser, area_id)

@area_router.get("/{area_id}/me", response_model=list[AreaResponse])
def get_user_areas_router(db: db, currUser: currUser):
    return get_user_areas(db, currUser)

@area_router.get("/{area_id}/members", response_model=list[UserResponse])
def get_area_user_members_router(db: db, area_id:int):
    return get_area_user_members(db, area_id)

@area_router.get("/{area_users}/user_id")
def get_user_areauser(db:db, user_id:int, area_id:int):
    return get_user_areauser(db, user_id, area_id)

@area_router.get("/{area_users}")
def get_area_user_router(db: db, currUser: currUser, area_id: int):
    return get_area_user(db, currUser, area_id)

@area_router.post("/{area_id}/users", response_model=AreaResponse)
def add_area_users_router(db: db, currUser: currUser, area_id: int, newMember_id: int | None = None):
    return add_area_users(db, currUser, area_id, newMember_id)

@area_router.patch("/{area_id}/users/me", response_model= AreaResponse)
def remove_area_users_router(db: db, currUser: currUser, area_id: int, newOwner_id: int | None = None):
    return remove_area_users(db, currUser, area_id, newOwner_id)

@area_router.delete("/{area_id}", response_model=AreaResponse)
def delete_area_router(db:db, currUser: currUser, area_id: int):
    return delete_area(db, currUser, area_id)