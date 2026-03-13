from __future__ import annotations
from typing import dataclass_transform
import enum
from sqlalchemy import Text, String, ForeignKey, DateTime, Time,  UniqueConstraint, func, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from datetime import datetime, time

@dataclass_transform()
class Base(DeclarativeBase):
    pass 

class TASKSTATUS(enum.Enum):
    NEEDS_ACTION = "NEEDS-ACTION"
    IN_PROCESS = "IN-PROCESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED" 
    
class SCHEDULESTATUS(enum.Enum):
    ACTIVE = "ACTIVE"
    PAUSED = 'PAUSED'
    COMPLETED = "COMPLETED"
    EXPIRED = "EXPIRED"


class AreaUser(Base):
    __tablename__ = "area_users"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    area_id: Mapped[int] = mapped_column(ForeignKey("areas.id"), primary_key=True)
    role: Mapped[str] = mapped_column(String(255), default="member")

class User(Base):
    __tablename__ = "users"
    # __table_args__ = (CheckConstraint("auth0_id IS NOT NULL OR discord_id IS NOT NULL", name="ck_user_has_one_identity"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    auth0_id: Mapped[str] = mapped_column(String(255), unique=True)
    #discord_id: Mapped[str | None] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    areas: Mapped[list[Area]] = relationship(secondary="area_users", back_populates="users")

class Area(Base):
    __tablename__ = "areas"
    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(255))
    users: Mapped[list[User]] = relationship(secondary="area_users", back_populates="areas")
    area_tasks: Mapped[list[AreaTask]] = relationship(back_populates="area", cascade="all, delete-orphan")

class TaskGroup(Base):
    __tablename__ = "task_groups"
    __table_args__ = (UniqueConstraint("name", "area_id", name="uq_taskgroup_name_per_area"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    area_id: Mapped[int] = mapped_column(ForeignKey("areas.id"))
    name: Mapped[str] = mapped_column(String(255))
    desc: Mapped[str | None] = mapped_column(Text)
    area_tasks: Mapped[list[AreaTask]] = relationship(back_populates="task_group")

class AreaTask(Base):
    __tablename__ = "area_tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    area_id: Mapped[int] = mapped_column(ForeignKey("areas.id"))
    task_group_id: Mapped[int | None] = mapped_column(ForeignKey('task_groups.id'))
    name: Mapped[str] = mapped_column(String(255))
    desc: Mapped[str | None] = mapped_column(Text)
    status: Mapped[TASKSTATUS] = mapped_column(default=TASKSTATUS.NEEDS_ACTION)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("area_tasks.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    schedule: Mapped[Schedule | None] = relationship(back_populates= "area_task", uselist=False, cascade="all, delete-orphan")
    area: Mapped[Area] = relationship(back_populates="area_tasks")
    task_group: Mapped[TaskGroup | None] = relationship(back_populates="area_tasks")
    parent_task: Mapped[AreaTask | None] = relationship(back_populates="subtasks", remote_side=[id])
    subtasks: Mapped[list[AreaTask]] = relationship(back_populates="parent_task", cascade="all, delete-orphan")

class Schedule(Base):
    __tablename__ = "schedules"
    id: Mapped[int] = mapped_column(primary_key=True)
    area_task_id: Mapped[int] = mapped_column(ForeignKey("area_tasks.id"), unique=True)
    rrule: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[SCHEDULESTATUS] = mapped_column(default=SCHEDULESTATUS.ACTIVE) 
    recurring: Mapped[bool] = mapped_column(default=False)
    c_provider: Mapped[str | None] = mapped_column(String(255))
    c_eventid: Mapped[str | None] = mapped_column(String(255))
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    due_time: Mapped[time] = mapped_column(Time, server_default="09:00:00")
    next_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    complete_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    area_task: Mapped[AreaTask] = relationship(back_populates="schedule")