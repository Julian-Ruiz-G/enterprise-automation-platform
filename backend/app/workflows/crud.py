from sqlalchemy.orm import Session

from app.workflows.models import Workflow

from app.workflows.schemas import WorkflowCreate, WorkflowUpdate


def create_workflow(
    db: Session,
    workflow: WorkflowCreate
):
    db.add(workflow)
    db.commit()
    db.refresh(workflow)
    return workflow

def get_workflows(
    db: Session,
    skip: int = 0,
    limit: int = 100
):
    return (
        db.query(Workflow)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_workflow_by_id(
    db: Session,
    workflow_id: int
):
    return (
        db.query(Workflow)
        .filter(
            Workflow.id == workflow_id
        )
        .first()
    )   
    

def get_workflows_by_trigger(
    db: Session,
    trigger: str
):
    return (
        db.query(Workflow)
        .filter(
            Workflow.trigger == trigger,
            Workflow.status == "ACTIVE"
        )
        .all()
    )


def get_workflow_by_name(
    db: Session,
    name: str
):
    return (
        db.query(Workflow)
        .filter(Workflow.name == name)
        .first()
    )

def update_workflow(
    db: Session,
    workflow: WorkflowUpdate
):
    db.commit()
    db.refresh(workflow)
    return workflow


def delete_workflow(
    db: Session,
    workflow: Workflow
):

    db.delete(workflow)
    db.commit()
