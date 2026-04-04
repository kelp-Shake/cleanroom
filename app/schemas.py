from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    name: str
    
class UserResponse(BaseModel):
    name: str 
    model_config = ConfigDict(from_attributes=True)

class AreaCreate(BaseModel):
    name: str

class AreaResponse(BaseModel):
    id: int
    name: str 
    model_config = ConfigDict(from_attributes=True)


class TaskGroupCreate(BaseModel):
    task_id: int
    owner_id: int
    name: str 

