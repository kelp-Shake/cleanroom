from fastapi import Depends, FastAPI
from app.auth import auth0
from app.user_routers import user_router
from app.area_router import area_router
from app.task_router import task_router
from app.schedule_router import schedule_router

appy = FastAPI()
appy.include_router(user_router, prefix="/users", tags = ["users"])
appy.include_router(area_router, prefix="/areas", tags = ["area"])
appy.include_router(task_router, prefix="/tasks", tags = ["task"])
appy.include_router(schedule_router, prefix="/schedule", tags = ["schedule"])

@appy.get("/api/public")
async def public():
    return {
        "message": "Hello from a public endpoint! You don't need to be authenticated to see this."
    }

@appy.get("/api/private")
async def private(claims: dict = Depends(auth0.require_auth())):
    return {
        "message": "Hello from a private endpoint! You need to be authenticated to see this.",
        "user_id": claims.get("sub")
    }

@appy.get("/api/private-scoped")
async def private_scoped(claims: dict = Depends(auth0.require_auth(scopes="read:messages"))):
    return {
        "message": "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this.",
        "user_id": claims.get("sub")
    }