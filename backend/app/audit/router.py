from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.audit.schemas import AuditLogResponse
from app.audit.service import list_logs

from app.security.dependencies import require_role_name

router = APIRouter(

    prefix="/audit",
    tags=["Audit"]

)


@router.get(
    "",
    response_model=list[AuditLogResponse]
)
def get_logs(

    skip: int = 0,
    limit: int = 100,

    db: Session = Depends(get_db),

    current_user=Depends(require_role_name("Administrador"))

):

    return list_logs(
        db,
        skip,
        limit
    )