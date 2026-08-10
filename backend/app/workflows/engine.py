from sqlalchemy.orm import Session
from app.workflows import crud
from app.workflows.actions import execute_action
from app.workflow_engine.actions.email_action import send_email
from app.notifications.service import execute_notification



def run_workflow(
    db: Session,
    trigger: str,
    payload: dict
):
    print("========== ENGINE ==========")
    print("Trigger recibido:", trigger)

    workflows = crud.get_workflows_by_trigger(
        db,
        trigger
    )

    print("Workflows encontrados:", len(workflows))

    for workflow in workflows:

        execute_notification(
            workflow.action,
            payload
        )

