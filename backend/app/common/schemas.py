from app.common.enums import (
    TicketStatus,
    TicketPriority,
    TicketChannel
)

class TicketCreate(BaseModel):
    title: str
    description: str
    status: TicketStatus
    priority: TicketPriority
    channel: TicketChannel
    client_id: int
    assigned_user_id: int | None = None