from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):

    id: int
    table_name: str
    record_id: int
    action: str
    user_id: int

    old_values: dict | None = None
    new_values: dict | None = None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )