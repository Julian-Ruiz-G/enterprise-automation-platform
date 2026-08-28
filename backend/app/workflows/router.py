from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.security.dependencies import require_role_name

from app.workflows.schemas import (
    WorkflowBase,
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowResponse
)

from app.workflows.service import (
    register_workflow,
    list_workflows,
    get_workflow,
    update_workflow,
    remove_workflow
)

router = APIRouter(
    prefix="/workflows",
    tags=["Workflows"]
)


@router.post(
    "",
    response_model=WorkflowResponse
)
def create_workflow(
    workflow: WorkflowBase,
    db: Session = Depends(get_db),
    current_user=Depends(require_role_name("Administrador"))
):
    return register_workflow(
        db,
        workflow
    )

@router.get(
    "",
    response_model=list[WorkflowResponse]
)
def get_workflows(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_role_name("Administrador"))
):
    return list_workflows(
        db,
        skip,
        limit
    )

@router.get(
    "/{workflow_id}",
    response_model=WorkflowResponse
)
def get_workflow_by_id(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role_name("Administrador"))
):
    return get_workflow(
        db,
        workflow_id
    )

@router.put(
    "/{workflow_id}",
    response_model=WorkflowResponse
)
def edit_workflow(
    workflow_id: int,
    workflow: WorkflowUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role_name("Administrador"))
):
    return update_workflow(
        db,
        workflow_id,
        workflow
    )

@router.delete(
    "/{workflow_id}"
)
def delete_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role_name("Administrador"))
):
    return remove_workflow(
        db,
        workflow_id
    )