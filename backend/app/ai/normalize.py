from app.common.enums import TicketCategory, TicketPriority

CATEGORY_ALIASES = {
    "facturacion": TicketCategory.BILLING,
    "facturación": TicketCategory.BILLING,
    "billing": TicketCategory.BILLING,
    "soporte": TicketCategory.SUPPORT,
    "support": TicketCategory.SUPPORT,
    "ventas": TicketCategory.SALES,
    "sales": TicketCategory.SALES,
}

PRIORITY_ALIASES = {
    "baja": TicketPriority.LOW,
    "low": TicketPriority.LOW,
    "media": TicketPriority.MEDIUM,
    "medium": TicketPriority.MEDIUM,
    "alta": TicketPriority.HIGH,
    "high": TicketPriority.HIGH,
    "urgente": TicketPriority.CRITICAL,
    "critical": TicketPriority.CRITICAL,
    "critica": TicketPriority.CRITICAL,
    "crítica": TicketPriority.CRITICAL,
}


def _key(value: str | None) -> str:
    if not value:
        return ""
    return value.strip().lower()


def normalize_category(raw: str | None) -> TicketCategory:
    return CATEGORY_ALIASES.get(_key(raw), TicketCategory.SUPPORT)


def normalize_priority(raw: str | None) -> TicketPriority:
    return PRIORITY_ALIASES.get(_key(raw), TicketPriority.MEDIUM)