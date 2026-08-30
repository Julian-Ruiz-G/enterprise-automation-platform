import logging

from sqlalchemy.orm import Session

from app.notifications.service import execute_notification
from app.workflows import crud

logger = logging.getLogger(__name__)



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

    logger.info("Workflows encontrados: %s", len(workflows))

    for workflow in workflows:
        try:
            execute_notification(workflow.action, payload)
            logger.info("Workflow ok id=%s action=%s", 
            workflow.id, 
            workflow.action)

        except Exception:
            logger.exception(
                "Worflow failed id=%s action=%s", 
                workflow.id, 
                workflow.action
            )

