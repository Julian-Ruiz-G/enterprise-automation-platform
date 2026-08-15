from pydantic import BaseModel
from datetime import datetime


class TicketAnalysis(BaseModel):
    categoria: str
    prioridad: str
    resumen: str
    respuesta: str
    sugerencias: str

    
class TicketCreate(BaseModel):
    title: str
    description: str
    status: str
    channel: str
    client_id: int


class TicketUpdate(BaseModel):

    title: str 
    description: str 
    status: str 
    priority: str 
    channel: str 
    client_id: int 
    assigned_user_id: int 
    category: str 
    sla_due_at: datetime | None = None
    first_response_at: datetime | None = None
    ai_summary: str | None = None
    ai_response: str | None = None


class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str
    channel: str
    client_id: int
    assigned_user_id: int
    category: str
    sla_due_at: datetime | None = None
    first_response_at: datetime | None = None
    ai_summary: str | None = None
    ai_response: str | None = None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True