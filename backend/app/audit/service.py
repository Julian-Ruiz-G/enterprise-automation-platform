from sqlalchemy.orm import Session

from app.audit.models import AuditLog
from app.audit import crud
from app.audit.utils import get_changes


def register_log(
    db: Session,
    table_name: str,
    record_id: int,
    action: str,
    user_id: int,
    old_values: dict | None = None,
    new_values: dict | None = None
):

    log = AuditLog(

        table_name=table_name,
        record_id=record_id,
        action=action,
        user_id=user_id,

        old_values=old_values,
        new_values=new_values
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