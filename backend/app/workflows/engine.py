import logging

from sqlalchemy.orm import Session

from app.notifications.service import execute_notification
from app.workflows import crud
import json

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

    print("Workflows encontrados:", len(workflows))
    for workflow in workflows:
        print("workflow id=", workflow.id, "config=", repr(workflow.configuration))

    for workflow in workflows:
        if not _matches_configuration(workflow, payload):
            print("skip", workflow.id)
            continue
        try:
            execute_notification(workflow.action, payload)
            print("ok", workflow.id, workflow.action)
        except Exception:
            logger.exception(
                "Worflow failed id=%s action=%s",
                workflow.id,
                workflow.action
            )


def _matches_configuration(workflow, payload: dict) -> bool:
    raw = (workflow.configuration or "").strip()
    if not raw:
        return True
    try:
        rules = json.loads(raw)
    except json.JSONDecodeError:
        logger.warning(
            "workflow id=%s configuration no es JSON: %s",
            workflow.id,
            raw,
        )
        return False
    if not isinstance(rules, dict):
        return False
    for key, expected in rules.items():
        if payload.get(key) != expected:
            return False
    return True
