from fastapi_plugin.fast_api_client import Auth0FastAPI
from sqlalchemy import select 
from app.db import curr_session
from app.models import User
from typing import Annotated
from fastapi import Depends, HTTPException
from dotenv import load_dotenv
import os
load_dotenv()
DOMAIN = os.environ['auth0_domain']
AUDIENCE = os.environ['auth0_api_aud']
auth0 = Auth0FastAPI(domain=DOMAIN, audience=AUDIENCE)
claims = Annotated[dict, Depends(auth0.require_auth())]
def get_CurrUser(claims: claims, db: curr_session) -> User:
    auth_id = claims.get("sub")
    state = select(User).where(User.auth0_id == auth_id)
    user = db.scalars(state).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
currUser = Annotated[User, Depends(get_CurrUser)]

