from app.notifications.email import send_email
from app.notifications.telegram import send_telegram
from app.notifications.whatsapp import send_whatsapp


def execute_notification(action: str, payload: dict):

    if action == "SEND_EMAIL":
        send_email(payload)

    elif action == "SEND_TELEGRAM":
        send_telegram(payload)

    elif action == "SEND_WHATSAPP":
        send_whatsapp(payload)

    else:
        print(f"Acción desconocida: {action}")