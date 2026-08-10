from app.workflows.models import Workflow

def execute_action(
    workflow: Workflow,
    payload: dict
):

    print("==============")
    print("Workflow:", workflow.name)
    print("Trigger:", workflow.trigger)
    print("Payload:", payload)
    print("==============")

    