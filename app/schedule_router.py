from fastapi import APIRouter
from app.db import curr_session as db 
from app.auth import currUser
from app.services.schedule import create_schedule, get_schedule, update_time, update_freq, update_status, delete_schedule
from datetime import datetime
from app.models import SCHEDULESTATUS
schedule_router = APIRouter()

@schedule_router.post("/")
def create_schedule_router(db: db, currUser: currUser, area_id: int, area_task_id:int, start_date: datetime):
    return create_schedule(db, currUser, area_id, area_task_id, start_date)

@schedule_router.get("/{schedule_id}")
def get_schedule_router(db: db, currUser: currUser, area_id: int, area_task_id:int, schedule_id:int):
    return get_schedule(db, currUser, area_id, area_task_id, schedule_id)

@schedule_router.post("/{schedule_id}/time")
def update_time_router(db: db,  currUser: currUser, area_id: int, area_task_id: int,  schedule_id: int, time_parms: dict):
    return update_time(db, currUser, area_id, area_task_id, schedule_id, time_parms)

@schedule_router.post("/{schedule_id}/freq")
def update_freq_router(db: db, currUser: currUser, area_id: int, area_task_id: int, schedule_id:int, recurring: bool, rrule: str | None = None):
    return update_freq(db, currUser, area_id, area_task_id, schedule_id, recurring, rrule)

@schedule_router.post("/{schedule_id}/status")
def update_status_router(db: db, currUser: currUser, area_id: int, area_task_id: int, schedule_id: int, sch_status: SCHEDULESTATUS):   
    return update_status(db, currUser, area_id, area_task_id, schedule_id, sch_status)              

@schedule_router.delete("/{schedule_id}")
def delete_schedule_router(db: db, currUser: currUser, area_id: int, area_task_id: int, schedule_id: int):
    return delete_schedule(db, currUser, area_id, area_task_id, schedule_id)