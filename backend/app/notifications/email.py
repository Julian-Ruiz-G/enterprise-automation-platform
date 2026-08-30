import logging

logger = logging.getLogger(__name__)

def send_email(payload: dict):
    logger.info(
        "SEND_EMAIL ticket_id=%s client_id=%s title=%s",
        payload.get("ticket_id"),
        payload.get("client_id"),
        payload.get("title"),
    )