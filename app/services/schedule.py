from sqlalchemy import select
from fastapi import HTTPException
from app.db import curr_session as db
from app.services.task import get_area_task
from app.models import Schedule, SCHEDULESTATUS
from app.auth import currUser
from dateutil.rrule import rrulestr
from datetime import datetime, time, timezone


#time_parms = {"start_date": (datetime | type(None)), "next_date": (datetime | type(None)), "due_time": time }

def create_schedule(db: db, currUser: currUser, area_id: int, area_task_id:int, start_date: datetime):
    area_task = get_area_task(db, currUser, area_id, area_task_id)
    if not area_task:
        raise HTTPException(status_code=400, detail="area task doesnt exsit")
    schedule = Schedule(start_date=start_date, area_task_id = area_task_id)
    db.add(schedule)
    db.flush()
    db.commit()
    return schedule 

def get_schedule(db: db, currUser: currUser, area_id: int, area_task_id:int, schedule_id:int):
    area_task = get_area_task(db, currUser, area_id, area_task_id)
    if not area_task:
        raise HTTPException(status_code=400, detail="area task doesnt exsit")
    # need match currusers area_tasks_ids but subtasks will have there own area_task_id 
    state = select(Schedule).where(Schedule.area_task_id == area_task_id, Schedule.id == schedule_id)
    schedule = db.scalar(state)
    return schedule 

def update_time(db: db,  currUser: currUser, area_id: int, area_task_id: int,  schedule_id: int, time_parms: dict):
    #validate scheduke
    valid_time = {"start_date": datetime, "due_time": time }
    schedule = get_schedule(db, currUser, area_id, area_task_id, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="schedule not found")
    #filter parms from 
    for key, val in time_parms.items():
        if key in valid_time and type(val) == valid_time[key]:
            setattr(schedule, key, val)
    db.add(schedule)
    db.commit()
    return schedule

def update_freq(db: db, currUser: currUser, area_id: int, area_task_id: int, schedule_id:int, reccuring: bool, rrule: str | None = None):
    schedule = get_schedule(db, currUser, area_id, area_task_id, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="schedule not found")
    if rrule == None:
        schedule.recurring = False 
    else:
        schedule.recurring = True
        schedule.rrule = rrule
        curr_next = rrulestr(rrule, dtstart=schedule.start_date).after(datetime.now(timezone.utc))
        if curr_next:
            schedule.next_date = curr_next
    db.add(schedule)
    db.commit()
    return schedule 

def update_status(db: db, currUser: currUser, area_id: int, area_task_id: int, schedule_id: int, sch_status: SCHEDULESTATUS):
    schedule = get_schedule(db, currUser, area_id, area_task_id, schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="schedule not found")
    if sch_status == SCHEDULESTATUS.COMPLETED:
        if schedule.recurring and schedule.rrule:
            curr_next = rrulestr(schedule.rrule, dtstart=schedule.start_date).after(datetime.now(timezone.utc))
            schedule.complete_at = datetime.now(timezone.utc)
            if curr_next:
                schedule.next_date = curr_next
            else:
                schedule.next_date = None 
                schedule.status = SCHEDULESTATUS.COMPLETED
        else:
            schedule.complete_at = datetime.now(timezone.utc)
            schedule.status = SCHEDULESTATUS.COMPLETED
    
    elif sch_status == SCHEDULESTATUS.ACTIVE:
        schedule.status = SCHEDULESTATUS.ACTIVE
    elif sch_status == SCHEDULESTATUS.PAUSED:
        schedule.status = SCHEDULESTATUS.PAUSED
    elif sch_status == SCHEDULESTATUS.EXPIRED:
        schedule.status = SCHEDULESTATUS.EXPIRED
    db.add(schedule)
    db.commit()
    return schedule

def delete_schedule(db: db, currUser: currUser, area_id: int, area_task_id: int, schedule_id: int):
    schedule = get_schedule(db, currUser, area_id, area_task_id, schedule_id)
    db.delete(schedule)
    db.commit()

    

# delete schedule (current, past, reccuring)
# delete 

# should a time be put on creation or auto (require fields) 
# create base: add area abd task area association
# update status, rrule, recurring(bool), due time, cproviders/events, startdate, complete at? (forgot how this changed)
# update schedule 
# rrule + reccuring -> del(rrule)=del(reccuring) update(start date) -> update(due time) if reccuring/rrule update 
# add remove (procider event id)
# scheule default (not reccuring) start time system end time 9 am current day (handle before 9 after 9 maybe default to next day)
# start/due time != date of week 
# diff between next date and complete at 
# think of day relations when creating a schedule 
# same day so list next date in the future 
# past due vs due 
# when complete at on change status (reccuring how does that effect complete at)
# rrule creates a date
# rrule: needs reeccuring to true
# status: def(active), paused -> no change, complete -> update if reccuring, expired -> complete at is status == complete
# reccuring needs rrule -> update next date 
# providers (not doing )
# start date, if none default else pass a date time 
# due time default if none else pass a time 
