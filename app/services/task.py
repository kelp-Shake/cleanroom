from sqlalchemy import select
from fastapi import HTTPException
from app.db import curr_session as db
from app.services.areas import get_area
from app.models import TaskGroup, AreaTask, TASKSTATUS
from app.auth import currUser

# task group
def create_task_group(db: db, currUser: currUser, name: str, desc: str|None = None):
    task_group = TaskGroup(owner_id = currUser.id, name = name, desc = desc)
    db.add(task_group)
    db.flush()
    db.commit()
    return task_group

def get_task_group(db:db, currUser:currUser, task_group_id: int):
    state = select(TaskGroup).where(TaskGroup.owner_id == currUser.id, TaskGroup.id == task_group_id)
    task_group = db.scalar(state)
    if not task_group:
        raise HTTPException(status_code=404, detail="not found")
    return task_group

def edit_task_group(db:db, currUser:currUser, task_group_id: int, name: str | None = None, desc: str | None = None):
    task_group = get_task_group(db, currUser, task_group_id)
    if not task_group:
        raise HTTPException(status_code=404, detail="not found")
    if name == None and str == None:
        raise HTTPException(status_code=408, detail="nothing was inputed")
    if name:
        task_group.name = name 
    if desc:
        task_group.desc = desc
    db.add(task_group)
    db.commit()
    return task_group

def delete_task_group(db: db, currUser: currUser, task_group_id: int):
    task_group = get_task_group(db, currUser, task_group_id)
    if not task_group:
        raise HTTPException(status_code=404, detail="not found")
    db.delete(task_group)
    db.commit()

def create_area_task(db:db, currUser: currUser, area_id: int, task_group_id: int, name: str, desc: str | None = None):
    area = get_area(db, currUser, area_id)
    task_group = get_task_group(db, currUser, task_group_id)
    if area and task_group:
        area_task = AreaTask(area_id=area.id, task_group_id=task_group.id, name=name, desc=desc)
        db.add(area_task)
        db.commit()
        return area_task
    else:
        raise HTTPException(status_code=408, detail="mising area id or task group id")
    
def get_area_task(db:db, currUser:currUser, area_id: int, area_task_id: int):
    area = get_area(db, currUser, area_id)
    if not area:
        raise HTTPException(status_code=404, detail="not found")
    state = select(AreaTask).where(AreaTask.id == area_task_id)
    area_task = db.scalar(state)
    if not area_task:
        raise HTTPException(status_code=404, detail="not found")
    return area_task

def create_sub_tasks(db:db, currUser:currUser, area_id: int, area_task_id: int,  sub_name:str, sub_desc: str| None = None, task_group_id: int | None = None):
    parent_area_task = get_area_task(db, currUser,area_id, area_task_id)
    if not parent_area_task:
        raise HTTPException(status_code=404, detail="not found")
    sub_task = AreaTask(area_id=area_id, parent_task=parent_area_task, name=sub_name, desc=sub_desc)
    if task_group_id:
        sub_task.task_group = get_task_group(db, currUser, task_group_id)
    db.add(sub_task)
    db.commit()
    return sub_task

def update_area_task(db: db, currUser: currUser, area_id: int, area_task_id: int, update_atts: dict):
    valid_update = {"name": str, "desc": (str, type(None)), "status": TASKSTATUS}
    area_task = get_area_task(db, currUser, area_id, area_task_id)
    for key, val in update_atts.items():
        if key in valid_update and isinstance(val, valid_update[key]):
            setattr(area_task, key, val)
    if update_atts.get("status") == TASKSTATUS.COMPLETED and area_task.subtasks:
        for subtask in area_task.subtasks:
            subtask.status = TASKSTATUS.COMPLETED
    db.add(area_task)
    db.commit()
    return area_task

def update_area_task_group(db: db, currUser: currUser, area_id: int, area_task_id: int, new_task_group_id: int):
    area_task = get_area_task(db, currUser, area_id, area_task_id)
    if not area_task:
        raise HTTPException(status_code=404, detail="not found")
    new_task_group = get_task_group(db, currUser, new_task_group_id)
    if new_task_group:
        area_task.task_group_id = new_task_group_id
    db.add(area_task)
    db.commit()
    return  area_task

def delete_area_task(db: db, currUser: currUser, area_id: int, area_task_id:int):
    area_task = get_area_task(db, currUser, area_id, area_task_id)
    db.delete(area_task)
    db.commit()
