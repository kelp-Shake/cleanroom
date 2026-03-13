from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    
class UserResponse(BaseModel):
    name: str | None
    
    model_config = ConfigDict(from_attributes=True)

# class AreaCreate(BaseModel):
#     name: str
# class AreaResponse(BaseModel):
#     pass
# class TaskGroupCreate(BaseModel):
#     name: str 

