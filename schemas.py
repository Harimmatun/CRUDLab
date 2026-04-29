from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class TaskBase(BaseModel):
    title: str
    description: str
    status: str = "TODO"

class TaskCreate(TaskBase):
    assignee_id: int

class TaskUpdate(BaseModel):
    status: str

class TaskResponse(TaskBase):
    id: int
    assignee_id: int
    model_config = ConfigDict(from_attributes=True)