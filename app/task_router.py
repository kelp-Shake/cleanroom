from fastapi import APIRouter
from app.db import curr_session as db 
from app.auth import currUser
from app.services.task import create_task_group, get_task_group, edit_task_group, delete_task_group, create_area_task, get_area_task, create_sub_tasks, update_area_task, update_area_task_group, delete_area_task
task_router = APIRouter()

@task_router.post("/")
def create_task_group_router(db: db, currUser:currUser, name: str, desc: str | None = None):
    return create_task_group(db, currUser, name, desc)

@task_router.get("/{task_group_id}")
def get_task_group_router(db: db, currUser: currUser, task_group_id: int):
    return get_task_group(db, currUser, task_group_id)
@task_router.patch("/{task_group_id}")
def edit_task_group_router(db: db, currUser: currUser, task_group_id: int, name: str | None = None, desc: str | None = None ):
    edit_task_group(db, currUser, task_group_id, name, desc)

@task_router.delete("/{task_group_id}")
def delete_task_group_router(db: db, currUser: currUser, task_group_id: int):
    return delete_task_group(db, currUser, task_group_id)

@task_router.post("/")
def create_area_task_router(db:db, currUser: currUser, area_id: int, task_group_id: int, name: str, desc: str | None = None):
    return create_area_task(db, currUser, area_id, task_group_id, name, desc)

@task_router.get("/{area_task_id}")
def get_area_task_router(db:db, currUser:currUser, area_id: int, area_task_id: int):
    return get_area_task(db, currUser, area_id, area_task_id)

@task_router.post("/{area_task_id}/subtasks")
def create_sub_tasks_router(db:db, currUser:currUser, area_id: int, area_task_id: int,  sub_name:str, sub_desc: str| None = None, task_group_id: int | None = None):
    return create_sub_tasks(db, currUser, area_id, area_task_id, sub_name, sub_desc)

@task_router.patch("/{area_task_id}")
def update_area_task_router(db: db, currUser: currUser, area_id: int, area_task_id: int, update_atts: dict):
    return update_area_task(db, currUser, area_id, area_task_id, update_atts)

@task_router.patch("/{area_task_id}/task_group")
def update_area_task_group_router(db: db, currUser: currUser, area_id: int, area_task_id: int, new_task_group_id: int):
    return update_area_task_group(db, currUser, area_id, area_task_id, new_task_group_id)

@task_router.delete("/{area_task_id}")
def delete_area_task_router(db: db, currUser: currUser, area_id: int, area_task_id:int):
    return delete_area_task(db, currUser, area_id, area_task_id)