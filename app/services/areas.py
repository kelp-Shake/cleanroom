from sqlalchemy import select
from fastapi import HTTPException
from app.db import curr_session as db
from app.models import User, Area, AreaUser, TaskGroup, AreaTask, Schedule, ROLES
from app.auth import currUser
from datetime import datetime, time

def create_area(db: db, currUser: currUser, name: str) -> Area:
    area = Area(name = name, owner_id=currUser.id)
    db.add(area)
    db.flush()
    new_area_user = AreaUser(user_id=currUser.id, area_id=area.id, role=ROLES.OWNER)
    db.add(new_area_user)
    db.commit()
    db.refresh(area)
    return area

def get_area(db: db, area_id: int) -> Area:
    state = select(Area).where(Area.id == area_id)
    area = db.scalars(state).first()
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    return area

def remove_area_user(db: db, currUser: currUser, currArea: Area, newOwner: User| None = None):
    pass

        

def get_area_user(db: db, currUser: currUser, currArea: Area):
    pass
    
def update_area_membership():
    pass

def delete_area():
    pass