from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TicketCommentCreate(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    is_internal: bool = False


class TicketCommentResponse(BaseModel):
    id: int
    ticket_id: int
    user_id: int
    client_id: int
    message: str
    is_internal: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
