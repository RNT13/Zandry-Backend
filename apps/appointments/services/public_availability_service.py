from __future__ import annotations

from datetime import date as date_cls
from datetime import timedelta
from typing import Iterable, Literal

from django.utils import timezone
from rest_framework.exceptions import ValidationError

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

SlotStatus = Literal["free", "busy"]


def _parse_hhmm(value: str) -> int:
    hours, minutes = value.split(":")
    return int(hours) * 60 + int(minutes)


def _format_hhmm(total_minutes: int) -> str:
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours:02d}:{minutes:02d}"


def _time_to_minutes(value) -> int:
    return value.hour * 60 + value.minute


def _get_weekday_code(day_date: date_cls) -> str:
    return WEEKDAY_BY_INDEX[day_date.weekday()]


def _get_business_hour(company: Company, weekday_code: str) -> BusinessHour | None:
    return BusinessHour.objects.filter(
        company=company,
        week_day=weekday_code,
        is_open=True,
    ).first()


def _intervals_overlap(start_a: int, end_a: int, start_b: int, end_b: int) -> bool:
    return start_a < end_b and end_a > start_b


def _booking_duration_minutes(booking: Appointment) -> int:
    service = getattr(booking, "service", None)
    if service and getattr(service, "duration", None) is not None:
        return int(service.duration)

    raw = getattr(booking, "service_duration", None)
    return int(raw) if raw is not None else 0


def _booking_time_start_minutes(booking: Appointment) -> int:
    booking_time = getattr(booking, "time", None)
    if not booking_time:
        return 0
    return _time_to_minutes(booking_time)


def _get_blocking_bookings(
    company: Company,
    day_date: date_cls,
    professional: Professional | None = None,
) -> Iterable[Appointment]:
    qs = Appointment.objects.filter(
        company=company,
        date=day_date,
        status__in=["pending", "confirmed"],
    )

    if professional is not None:
        qs = qs.filter(professional=professional)

    return qs.select_related("service")


def _build_blocked_intervals(
    company: Company,
    day_date: date_cls,
    professional: Professional | None = None,
) -> list[tuple[int, int]]:
    blocked_intervals: list[tuple[int, int]] = []

    for booking in _get_blocking_bookings(company, day_date, professional):
        booking_start = _booking_time_start_minutes(booking)
        booking_end = booking_start + _booking_duration_minutes(booking)
        blocked_intervals.append((booking_start, booking_end))

    return blocked_intervals


def _slot_conflicts_with_bookings(
    start_min: int,
    end_min: int,
    blocked_intervals: list[tuple[int, int]],
) -> bool:
    return any(
        _intervals_overlap(start_min, end_min, booked_start, booked_end)
        for booked_start, booked_end in blocked_intervals
    )


def _is_past_slot(day_date: date_cls, start_min: int) -> bool:
    now = timezone.localtime(timezone.now())
    today = timezone.localdate()
    current_now_minutes = now.hour * 60 + now.minute

    if day_date < today:
        return True

    if day_date == today and start_min <= current_now_minutes:
        return True

    return False


def _can_schedule_slot(
    *,
    company: Company,
    service: Service,
    day_date: date_cls,
    start_min: int,
    professional: Professional | None = None,
) -> bool:
    weekday_code = _get_weekday_code(day_date)
    business_hour = _get_business_hour(company, weekday_code)

    if not business_hour or not business_hour.start or not business_hour.end:
        return False

    business_start = _parse_hhmm(business_hour.start)
    business_end = _parse_hhmm(business_hour.end)
    duration_min = int(service.duration)

    if duration_min <= 0:
        return False

    end_min = start_min + duration_min

    if start_min < business_start:
        return False

    if end_min > business_end:
        return False

    if _is_past_slot(day_date, start_min):
        return False

    blocked_intervals = _build_blocked_intervals(company, day_date, professional)
    if _slot_conflicts_with_bookings(start_min, end_min, blocked_intervals):
        return False

    return True


def validate_public_booking_slot(
    *,
    company: Company,
    service: Service,
    professional: Professional,
    booking_date: date_cls,
    booking_time,
) -> None:
    start_min = _time_to_minutes(booking_time)
    weekday_code = _get_weekday_code(booking_date)
    business_hour = _get_business_hour(company, weekday_code)

    if not business_hour or not business_hour.start or not business_hour.end:
        raise ValidationError({"time": "A empresa não atende neste dia."})

    duration_min = int(service.duration)
    if duration_min <= 0:
        raise ValidationError({"time": "Duração de serviço inválida."})

    business_start = _parse_hhmm(business_hour.start)
    business_end = _parse_hhmm(business_hour.end)
    end_min = start_min + duration_min

    if start_min < business_start:
        raise ValidationError({"time": "Esse horário começa antes do funcionamento da empresa."})

    if end_min > business_end:
        raise ValidationError({"time": "Esse horário não comporta a duração total do serviço."})

    if _is_past_slot(booking_date, start_min):
        raise ValidationError({"time": "Esse horário já passou."})

    blocked_intervals = _build_blocked_intervals(company, booking_date, professional)
    if _slot_conflicts_with_bookings(start_min, end_min, blocked_intervals):
        raise ValidationError({"time": "Este horário já está reservado. Escolha outro."})


def _build_slot_status(
    *,
    start_min: int,
    blocked_intervals: list[tuple[int, int]],
) -> SlotStatus:
    slot_end = start_min + SLOT_STEP_MINUTES
    slot_busy = _slot_conflicts_with_bookings(start_min, slot_end, blocked_intervals)
    return "busy" if slot_busy else "free"


def _build_day_slots(
    *,
    company: Company,
    service: Service,
    day_date: date_cls,
    professional: Professional | None = None,
) -> dict:
    weekday_code = _get_weekday_code(day_date)
    business_hour = _get_business_hour(company, weekday_code)

    if not business_hour or not business_hour.start or not business_hour.end:
        return {
            "date": day_date,
            "label": day_date.strftime("%d/%m"),
            "weekday": weekday_code,
            "is_open": False,
            "slots": [],
        }

    business_start_min = _parse_hhmm(business_hour.start)
    business_end_min = _parse_hhmm(business_hour.end)
    duration_min = int(service.duration)

    if business_start_min >= business_end_min or duration_min <= 0:
        return {
            "date": day_date,
            "label": day_date.strftime("%d/%m"),
            "weekday": weekday_code,
            "is_open": True,
            "slots": [],
        }

    blocked_intervals = _build_blocked_intervals(company, day_date, professional)

    slots: list[dict] = []
    current_start = business_start_min

    while current_start < business_end_min:
        if _is_past_slot(day_date, current_start):
            current_start += SLOT_STEP_MINUTES
            continue

        slot_end_if_service = current_start + duration_min
        ends_at = _format_hhmm(slot_end_if_service)

        slot_busy = (
            _build_slot_status(
                start_min=current_start,
                blocked_intervals=blocked_intervals,
            )
            == "busy"
        )

        fits_in_business = slot_end_if_service <= business_end_min
        no_conflict = not _slot_conflicts_with_bookings(
            current_start,
            slot_end_if_service,
            blocked_intervals,
        )

        available = fits_in_business and no_conflict
        conflict = (not available) and not slot_busy

        slots.append(
            {
                "date": day_date,
                "time": _format_hhmm(current_start),
                "ends_at": ends_at,
                "available": available,
                "free": not slot_busy,
                "busy": slot_busy,
                "conflict": conflict,
            }
        )

        current_start += SLOT_STEP_MINUTES

    return {
        "date": day_date,
        "label": day_date.strftime("%d/%m"),
        "weekday": weekday_code,
        "is_open": True,
        "slots": slots,
    }


def build_public_availability(
    *,
    company: Company,
    service: Service,
    professional: Professional | None = None,
    date: date_cls | None = None,
) -> dict:
    if date:
        target_dates = [date]
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
