from datetime import date as date_cls, timedelta

from apps.appointments.models import Appointment
from apps.appointments.utils import generate_slots

WEEKDAY_MAP = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sunday",
}

SLOT_INTERVAL = 15


def slots_needed(duration_minutes: int) -> int:
    return -(-duration_minutes // SLOT_INTERVAL)


def build_public_availability(company, professional, service, start_day=None):
    n_slots = slots_needed(service.duration)
    start_day = start_day or date_cls.today()
    end_day = start_day + timedelta(days=7)

    booked_raw = Appointment.objects.filter(
        professional=professional,
        date__gte=start_day,
        date__lt=end_day,
        status__in=["pending", "confirmed"],
    ).values_list("date", "time")

    booked_set = {
        (d if isinstance(d, date_cls) else d.date(), t.strftime("%H:%M"))
        for d, t in booked_raw
    }

    days = []

    for i in range(7):
        current_day = start_day + timedelta(days=i)
        weekday_key = WEEKDAY_MAP[current_day.weekday()]

        bh = company.business_hours.filter(week_day=weekday_key, is_open=True).first()

        if not bh or not bh.start or not bh.end:
            days.append({
                "date": current_day,
                "label": current_day.strftime("%d/%m"),
                "weekday": weekday_key,
                "is_open": False,
                "slots": [],
            })
            continue

        all_times = generate_slots(bh.start, bh.end, interval_minutes=SLOT_INTERVAL)

        slots = []
        for idx, time_str in enumerate(all_times):
            directly_booked = (current_day, time_str) in booked_set
            fits_in_window = (idx + n_slots) <= len(all_times)
            future_slots_blocked = any(
                (current_day, all_times[idx + offset]) in booked_set
                for offset in range(n_slots)
                if (idx + offset) < len(all_times)
            )

            available = not directly_booked and fits_in_window and not future_slots_blocked

            slots.append({
                "date": current_day,
                "time": time_str,
                "available": available,
            })

        days.append({
            "date": current_day,
            "label": current_day.strftime("%d/%m"),
            "weekday": weekday_key,
            "is_open": True,
            "slots": slots,
        })

    return {"days": days}
