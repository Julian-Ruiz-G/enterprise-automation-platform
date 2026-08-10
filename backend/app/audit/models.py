from sqlalchemy import (
    String,
    ForeignKey,
    DateTime,
    JSON,
    func
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database.base import Base


class AuditLog(Base):

    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    table_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    record_id: Mapped[int] = mapped_column(
        nullable=False
    )

    action: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    old_values: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )

    new_values: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

