from sqlalchemy import select
from fastapi import HTTPException
from app.db import curr_session as db
from app.models import User
from app.auth import currUser, claims
from app.schemas import UserCreate

def create_user(db: db, claims: claims, createUser: UserCreate) -> User:
    auth_id = claims.get("sub")
    state = select(User).where(User.auth0_id == auth_id)
    curr_user = db.scalars(state).first()
    if curr_user:
        raise HTTPException(status_code=400, detail= "This user account already exits")
    if auth_id == None:
        raise HTTPException(status_code=404, detail="no auth id")
    user = User(name = createUser.name, auth0_id=auth_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(user: currUser) -> User:
    return user

def update_user(db: db, currUser: currUser, updateUser: UserCreate) -> User:
    if updateUser.name is None and currUser.auth0_id is not None:
        raise HTTPException(status_code=400, detail="you must have a user name")
    if updateUser.name is not None:
        currUser.name = updateUser.name
    db.commit()
    db.refresh(currUser)
    return currUser