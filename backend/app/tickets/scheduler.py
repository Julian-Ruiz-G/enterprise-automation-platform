import asyncio
import logging

from app.core.config import settings
from app.database.database import SessionLocal
from app.tickets.service import check_sla_breaches

logger = logging.getLogger(__name__)


async def run_sla_loop() -> None:
    interval = settings.SLA_CHECK_INTERVAL_SECONDS
    while True:
        await asyncio.sleep(interval)
        db = SessionLocal()
        try:
            ids = check_sla_breaches(db)
            if ids:
                logger.info("sla loop tickets=%s", ids)
        except Exception:
            logger.exception("sla loop fallo")
        finally:
            db.close()