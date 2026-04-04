from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from app.db import curr_session as db
from app.models import User, Area, AreaUser, ROLES
from app.auth import currUser

# for the current user unless specified 
def create_area(db: db, currUser: currUser, name: str) -> Area:
    area = Area(name = name, owner_id=currUser.id)
    db.add(area)
    db.flush()
    new_area_user = AreaUser(user_id=currUser.id, area_id=area.id, role=ROLES.OWNER)
    db.add(new_area_user)
    db.commit()
    db.refresh(area)
    return area

def get_area(db: db, currUser: currUser, area_id: int) -> Area:
    state = select(Area).join(Area.users).where(Area.id == area_id, User.id == currUser.id)
    area = db.scalar(state)
    if not area:
        raise HTTPException(status_code=404, detail="not found")
    return area

def get_user_areas(db: db, currUser: currUser) -> list[Area]:
    state = select(Area).join(Area.users).where(User.id == currUser.id)
    user_areas = list(db.scalars(state).all())
    if not user_areas:
        raise HTTPException(status_code=404, detail="no areas found")
    return user_areas

def get_area_user_members(db: db, area_id: int) -> list[User]:
    state = select(Area).where(Area.id == area_id).options(selectinload(Area.users))
    area = db.scalar(state)
    if not area:
        raise HTTPException(status_code=404, detail="not found")
    return area.users

def get_user_areauser(db: db, user_id: int, area_id: int):
    state = select(AreaUser).where(AreaUser.area_id == area_id, AreaUser.user_id == user_id)
    user = db.scalar(state)
    return user

def get_area_user(db: db, currUser: currUser, area_id: int) -> AreaUser:
    state = select(AreaUser).where(AreaUser.area_id == area_id, AreaUser.user_id == currUser.id)
    area_user = db.scalar(state)
    if not area_user:
        raise HTTPException(status_code=400, detail="the user and area are not associated or it doesnt exsist")
    return area_user

def add_area_users(db: db, currUser: currUser, area_id: int, newMember_id: int | None = None):
    area = get_area(db, currUser, area_id)
    curr_user = get_area_user(db, currUser, area_id)
    if curr_user.role != ROLES.OWNER:
        raise HTTPException(status_code=403, detail="you are not the ownner")
    if not newMember_id:
        raise HTTPException(status_code=403, detail="you need to asign the area a new owner")
    is_member = get_user_areauser(db, newMember_id, area_id)
    if is_member:
        raise HTTPException(status_code=400, detail="user is already a memeber")
    new_area_user = AreaUser(user_id=newMember_id, area_id=area_id, role=ROLES.MEMBER)
    db.add(new_area_user)
    db.commit()
    return area 

def remove_area_users(db: db, currUser: currUser, area_id: int, newOwner_id : int | None = None):
    area_user = get_area_user(db, currUser,area_id)  
    area_members = get_area_user_members(db, area_id)
    if area_user.role == ROLES.OWNER:
        if len(area_members) < 2:
            delete_area(db, currUser, area_id)
            return 
        if not newOwner_id:
            raise HTTPException(status_code=403, detail="this area needs a new owner")
        new_owner = get_user_areauser(db, newOwner_id, area_id)
        if not new_owner:
            raise HTTPException(status_code=403, detail="this users isnt apart of the area")
        new_owner.role = ROLES.OWNER
    db.delete(area_user)
    db.commit()

def delete_area(db:db, currUser: currUser, area_id: int):
    area = get_area(db, currUser, area_id)
    area_user = get_area_user(db, currUser, area_id)
    if area_user.role == ROLES.MEMBER:
        raise HTTPException(status_code=400, detail="you area not the owner of this area")
    db.delete(area)
    db.commit()