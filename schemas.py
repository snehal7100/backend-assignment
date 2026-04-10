from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class Login(BaseModel):
    email: str
    password: str

class TaskCreate(BaseModel):
    title: str
    description: str
    deadline: str
    assigned_to: int
    status: str = "not_started"

class MoveTask(BaseModel):
    task_id: int
    new_status: str
    new_position: int