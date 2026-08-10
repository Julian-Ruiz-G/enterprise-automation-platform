from sqlalchemy import ForeignKey, String, DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class TicketComment(Base):
    __tablename__ = "ticket_comments"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    ticket_comment_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"),
        nullable=False
    )
    
    message: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )
    
    is_internal: Mapped[bool] = mapped_column(
        default=False,
        nullable=False
    )
    
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )