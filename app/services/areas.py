from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from app.db import curr_session as db
from app.models import User, Area, AreaUser, TaskGroup, AreaTask, Schedule
from app.auth import currUser
from app.schemas import UserCreate, UserUpdate
from datetime import datetime, time

# post: create
def create_user(db: db, auth_id: str | None, createUser: UserCreate) -> User:
    if auth_id == None:
        raise HTTPException(status_code=400, detail="auth id needed")
    user = User(name=createUser.name, auth0_id=auth_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_area(db: db, currUser: currUser, name: str) -> Area:
    area = Area(name = name, owner_id=currUser.id)
    db.add(area)
    db.flush()
    new_area_user = AreaUser(user_id=currUser.id, area_id=area.id, role="owner")
    db.add(new_area_user)
    db.commit()
    db.refresh(area)
    return area

def create_task_group(db: db, name: str, area_id: int, desc: str | None = None) -> TaskGroup:
    new_task_group = TaskGroup(area_id= area_id, name=name, desc=desc)
    db.add(new_task_group)
    db.commit()
    db.refresh(new_task_group)
    return new_task_group

def create_area_task(db:db, task_group_id: int, name: str, parent_id: int| None = None, desc: str | None = None) -> AreaTask:
    task_group = db.get(TaskGroup, task_group_id)
    if not task_group:
                raise HTTPException(status_code=404, detail="Task Group not found")
    new_area_task = AreaTask(name=name, parent_id=parent_id, desc=desc)
    db.add(new_area_task)
    db.commit()
    db.refresh(new_area_task)
    return new_area_task

def create_schedule(db: db, area_task_id: int, due_time: time, start_date: datetime| None = None) :
    area_task = db.get(AreaTask, area_task_id)
    if not area_task:
        raise HTTPException(status_code=404, detail="Area Task not found")
    if area_task.schedule:
         raise HTTPException(status_code=409, detail="Area Task already has a schedule, update schedule")

    new_schedule = Schedule(area_task_id=area_task_id, start_date=start_date if start_date is not None else datetime.now(),due_time=due_time if due_time is not None else time(9, 0))
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule


# get
def get_user(user: currUser) -> User:
    return user

def getArea(db: db, area_id: int) -> Area:
    state = select(Area).where(Area.id == area_id)
    area = db.scalars(state).first()
    if not area:
        raise HTTPException(status_code=404, detail="Area not found")
    return area



def get_area_user(db: db, currUser: currUser, currArea: Area):
    state = select(AreaUser).where(AreaUser.user_id == currUser.id, AreaUser.area_id == currArea.id)
    area_user = db.scalars(state).first()
    if not area_user:
        raise HTTPException(status_code=400, detail="the current user and area are not associated")
    return area_user

def get_task_group():
    pass
def get_schedule():
    pass


# put: update
# area, id1, id2 
def update_user(db: db, currUser: currUser, updateUser: UserUpdate) -> User:
    if updateUser.name is None and currUser.auth0_id is not None:
        raise HTTPException(status_code=400, detail="you must have a user name")
    if updateUser.name is not None:
        currUser.name = updateUser.name
    db.commit()
    db.refresh(currUser)
    return currUser

def update_area_membership():
    pass
def update_task_group():
    pass
def update_schedule():
    pass
def update_status():
    pass


# delete
def remove_area_user(db: db, currUser: currUser, currArea: Area, newOwner: User| None = None):
    area_user = get_area_user(db=db, currUser=currUser, currArea=currArea)
    if not area_user:
        raise HTTPException(status_code=404, detail="the current user and area does not exist")
def delete_schedule():
    pass
def delete_task_group():
    pass
def delete_area():
    pass
