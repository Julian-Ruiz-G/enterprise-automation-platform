from datetime import datetime
from pydantic import BaseModel, ConfigDict


class WorkflowBase(BaseModel):

    name: str

    description: str | None = None

    trigger: str

    action: str

    configuration: str | None = None

    status: str = ""



class WorkflowCreate(BaseModel):
    name: str
    description: str
    trigger: str
    action: str          # <-- agregar
    configuration: dict | None = None
    status: str


class WorkflowUpdate(BaseModel):

    name: str | None = None

    description: str | None = None

    trigger: str | None = None
    
    action: str 

    configuration: str | None = None

    status: str | None = None


class WorkflowResponse(BaseModel):

    id: int

    action: str

    created_at: datetime

    updated_at: datetime
    

    model_config = ConfigDict(from_attributes=True)