from sqlalchemy import ForeignKey, String, DateTime
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    
    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    priority: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    
    channel: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    
    client_id: Mapped[int] = mapped_column(
        ForeignKey("clients.id"),
        nullable=False
    )
    
    assigned_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True
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

    ai_category: Mapped[str | None] = mapped_column(
    String(100)
    )

    ai_priority: Mapped[str | None] = mapped_column(
        String(50)
    )

    ai_summary: Mapped[str | None] = mapped_column(
        String(500)
    )

    ai_response: Mapped[str | None] = mapped_column(
        String(1000)
    )

    sla_due_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))

    first_response_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
    
    closed_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))

    sla_alerted_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))