from pydantic import BaseModel, ConfigDict
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
    channel: str
    client_id: int
    status: str = "OPEN"
    assigned_user_id: int | None = None

class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    channel: str | None = None
    client_id: int | None = None
    assigned_user_id: int | None = None
    category: str | None = None
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
    assigned_user_id: int | None = None
    category: str
    sla_due_at: datetime | None = None
    first_response_at: datetime | None = None
    ai_summary: str | None = None
    ai_response: str | None = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)