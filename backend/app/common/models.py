from app.common.enums import (
    TicketStatus,
    TicketPriority,
    TicketChannel
)

status = Column(
    Enum(TicketStatus),
    nullable=False
)

priority = Column(
    Enum(TicketPriority),
    nullable=False
)

channel = Column(
    Enum(TicketChannel),
    nullable=False
)