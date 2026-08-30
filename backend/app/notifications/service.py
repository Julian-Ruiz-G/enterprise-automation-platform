import logging

from app.notifications.email import send_email
from app.notifications.telegram import send_telegram
from app.notifications.whatsapp import send_whatsapp

logger = logging.getLogger(__name__)


def execute_notification(action: str, payload: dict):

    if action == "SEND_EMAIL":
        send_email(payload)

    elif action == "SEND_TELEGRAM":
        send_telegram(payload)

    elif action == "SEND_WHATSAPP":
        send_whatsapp(payload)

    else:
        logger.warning("Acción de workflow desconocida: %s", action)