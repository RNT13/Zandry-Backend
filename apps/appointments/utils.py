from datetime import datetime, timedelta


def generate_slots(start: str, end: str, interval_minutes: int = 15) -> list[str]:
    """
    Gera lista de horários entre start e end com intervalo fixo.
    Ex: start="08:00", end="10:00", interval=15
    → ["08:00", "08:15", "08:30", "08:45", "09:00", "09:15", "09:30", "09:45"]
    Nota: end NÃO é incluído (o último slot começa antes do end).
    """
    fmt = "%H:%M"
    current = datetime.strptime(start, fmt)
    finish = datetime.strptime(end, fmt)
    slots = []

    while current < finish:
        slots.append(current.strftime(fmt))
        current += timedelta(minutes=interval_minutes)

    return slots
