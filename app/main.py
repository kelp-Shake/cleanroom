from fastapi import Depends, FastAPI
from app.auth import auth0
from app.routers import router as user_router

appy = FastAPI()
appy.include_router(user_router, prefix="/users", tags = ["users"])


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