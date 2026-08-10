from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.workflows import crud
from app.workflows.models import Workflow
from app.workflows.schemas import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowResponse,
    WorkflowBase
)

def register_workflow(
    db: Session,
    workflow: WorkflowBase
):
    existing = crud.get_workflow_by_name(
        db,
        workflow.name
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="El workflow ya existe"
        )
    
    db_workflow = Workflow(
        name=workflow.name,
        description=workflow.description,
        trigger=workflow.trigger,
        action=workflow.action,
        configuration=workflow.configuration,
        status=workflow.status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    return crud.create_workflow(
        db, 
        db_workflow
    )

def list_workflows(
    db: Session,
    skip: int,
    limit: int
):
    return crud.get_workflows(
        db,
        skip,
        limit
    )

def get_workflow(
    db: Session,
    workflow_id: int
):

    workflow = crud.get_workflow_by_id(
        db,
        workflow_id
    )

    if workflow is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow no encontrado"
        )

    return workflow


def update_workflow(
    db: Session,
    workflow_id: int,
    workflow_update: WorkflowUpdate
):

    workflow = crud.get_workflow_by_id(
        db,
        workflow_id
    )

    if workflow is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow no encontrado"
        )

    data = workflow_update.model_dump(
        exclude_unset=True
    )

    for key, value in data.items():
        setattr(
            workflow,
            key,
            value
        )

    return crud.update_workflow(
        db,
        workflow
    )

def remove_workflow(
    db: Session,
    workflow_id: int
):

    workflow = crud.get_workflow_by_id(
        db,
        workflow_id
    )

    if workflow is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow no encontrado"
        )

    crud.delete_workflow(
        db,
        workflow
    )

    return {
        "message": "Workflow eliminado correctamente"
    }