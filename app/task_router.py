from fastapi import APIRouter
from app.db import curr_session as db 
from app.models import TaskGroup, AreaTask
from app.services.task import create_task_group, get_task_group, edit_task_group, delete_task_group, create_area_task, get_area_task, create_sub_tasks, update_area_task, update_area_task_group, delete_area_task_stuff, delete_area_task
task_router = APIRouter()
