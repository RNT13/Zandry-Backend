from __future__ import annotations

from datetime import date as date_cls
from datetime import datetime, timedelta
from typing import Iterable

from django.utils import timezone

from apps.appointments.models import Appointment
from apps.companies.models import BusinessHour, Company
from apps.professionals.models import Professional
from apps.services.models import Service

SLOT_STEP_MINUTES = 15
LOOKAHEAD_DAYS = 14

WEEKDAY_BY_INDEX = {
    0: "monday",
    1: "tuesday",
    2: "wednesday",
    3: "thursday",
    4: "friday",
    5: "saturday",
    6: "sunday",
}

WEEKDAY_LABELS = {
    "monday": "Segunda-feira",
    "tuesday": "Terça-feira",
    "wednesday": "Quarta-feira",
    "thursday": "Quinta-feira",
    "friday": "Sexta-feira",
    "saturday": "Sábado",
    "sunday": "Domingo",
}


def _parse_hhmm(value: str) -> int:
    hours, minutes = value.split(":")
    return int(hours) * 60 + int(minutes)


def _format_hhmm(total_minutes: int) -> str:
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours:02d}:{minutes:02d}"


def _get_weekday_code(day_date: date_cls) -> str:
    return WEEKDAY_BY_INDEX[day_date.weekday()]


def _get_business_hour(company: Company, weekday_code: str) -> BusinessHour | None:
    return BusinessHour.objects.filter(company=company, week_day=weekday_code).first()


def _booking_duration_minutes(booking: Appointment) -> int:
    service = getattr(booking, "service", None)
    if service and getattr(service, "duration", None) is not None:
        return int(service.duration)

    # fallback caso seu booking armazene a duração em outro campo
    raw = getattr(booking, "service_duration", None)
    return int(raw) if raw is not None else 0


def _booking_time_start_minutes(booking: Appointment) -> int:
    booking_time = getattr(booking, "time", None)
    if not booking_time:
        return 0
    return _parse_hhmm(str(booking_time)[:5])


def _intervals_overlap(start_a: int, end_a: int, start_b: int, end_b: int) -> bool:
    return start_a < end_b and end_a > start_b


def _get_blocking_bookings(
    company: Company,
    day_date: date_cls,
    professional: Professional | None = None,
) -> Iterable[Appointment]:
    booking_qs = Appointment.objects.filter(company=company, date=day_date)

    field_names = {f.name for f in Appointment._meta.get_fields()}

    if "status" in field_names:
        booking_qs = booking_qs.exclude(status__in=["cancelled", "canceled"])

    if professional is not None and "professional" in field_names:
        booking_qs = booking_qs.filter(professional=professional)

    if "service" in field_names:
        booking_qs = booking_qs.select_related("service")

    return booking_qs


def _build_day_slots(
    *,
    company: Company,
    service: Service,
    day_date: date_cls,
    professional: Professional | None = None,
) -> dict:
    weekday_code = _get_weekday_code(day_date)
    business_hour = _get_business_hour(company, weekday_code)

    if not business_hour or not business_hour.is_open:
        return {
            "date": day_date.isoformat(),
            "label": WEEKDAY_LABELS[weekday_code],
            "weekday": weekday_code,
            "is_open": False,
            "slots": [],
        }

    if not business_hour.start or not business_hour.end:
        return {
            "date": day_date.isoformat(),
            "label": WEEKDAY_LABELS[weekday_code],
            "weekday": weekday_code,
            "is_open": False,
            "slots": [],
        }

    start_min = _parse_hhmm(business_hour.start)
    end_min = _parse_hhmm(business_hour.end)
    duration_min = int(service.duration)

    if start_min >= end_min or duration_min <= 0:
        return {
            "date": day_date.isoformat(),
            "label": WEEKDAY_LABELS[weekday_code],
            "weekday": weekday_code,
            "is_open": True,
            "slots": [],
        }

    now = timezone.localtime(timezone.now())
    today = timezone.localdate()

    blocking_bookings = list(_get_blocking_bookings(company, day_date, professional=professional))
    blocked_intervals: list[tuple[int, int]] = []

    for booking in blocking_bookings:
        booking_start = _booking_time_start_minutes(booking)
        booking_duration = _booking_duration_minutes(booking)
        booking_end = booking_start + booking_duration
        blocked_intervals.append((booking_start, booking_end))

    slots: list[dict] = []

    last_start = end_min - duration_min
    current_start = start_min

    while current_start <= last_start:
        slot_end = current_start + duration_min
        slot_time = _format_hhmm(current_start)

        is_past = False
        if day_date < today:
            is_past = True
        elif day_date == today:
            current_now_minutes = now.hour * 60 + now.minute
            is_past = current_start <= current_now_minutes

        overlaps_booking = any(
            _intervals_overlap(current_start, slot_end, booked_start, booked_end)
            for booked_start, booked_end in blocked_intervals
        )

        available = not is_past and not overlaps_booking

        slots.append(
            {
                "date": day_date.isoformat(),
                "time": slot_time,
                "available": available,
            }
        )

        current_start += SLOT_STEP_MINUTES

    return {
        "date": day_date.isoformat(),
        "label": WEEKDAY_LABELS[weekday_code],
        "weekday": weekday_code,
        "is_open": True,
        "slots": slots,
    }


def build_public_availability(
    *,
    company: Company,
    service: Service,
    professional: Professional | None = None,
    date: str | None = None,
) -> dict:
    """
    Retorna a disponibilidade em dias/slots.
    - Se `date` vier no querystring, retorna apenas esse dia.
    - Se não vier, retorna os próximos LOOKAHEAD_DAYS dias.
    """
    if date:
        target_dates = [datetime.strptime(date, "%Y-%m-%d").date()]
    else:
        today = timezone.localdate()
        target_dates = [today + timedelta(days=i) for i in range(LOOKAHEAD_DAYS)]

    days = [
        _build_day_slots(
            company=company,
            service=service,
            day_date=day_date,
            professional=professional,
        )
        for day_date in target_dates
    ]

    return {"days": days}
