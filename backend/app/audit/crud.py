from sqlalchemy.orm import Session

from app.audit.models import AuditLog


def create_log(
    db: Session,
    log: AuditLog
):

    db.add(log)
    db.commit()
    db.refresh(log)

    return log


def get_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100
):

    return (
        db.query(AuditLog)
        .offset(skip)
        .limit(limit)
        .all()
    )