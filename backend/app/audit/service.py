from sqlalchemy.orm import Session
from datetime import datetime, date

from app.audit.models import AuditLog
from app.audit import crud
from app.audit.utils import get_changes


def json_safe(value):
    if isinstance(value, dict):
        return {k: json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return value

def register_log(
    db: Session,
    table_name: str,
    record_id: int,
    action: str,
    user_id: int,
    old_values=None,
    new_values=None,
):

    log = AuditLog(

        table_name=table_name,
        record_id=record_id,
        action=action,
        user_id=user_id,

        old_values=json_safe(old_values) if old_values is not None else None,
        new_values=json_safe(new_values) if new_values is not None else None,
        created_at=datetime.now()
    )

    return crud.create_log(
        db,
        log
    )


def list_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100
):

    return crud.get_logs(
        db,
        skip,
        limit
    )


def register_update_log(
    db,
    table_name,
    old_record,
    new_record,
    user_id
):

    changes = get_changes(old_record, new_record)

    if not changes:
        return

    register_log(
        db=db,
        table_name=table_name,
        record_id=new_record.id,
        action="UPDATE",
        user_id=user_id,
        old_values=old_record.model_dump(),
        new_values=new_record.model_dump()
    )