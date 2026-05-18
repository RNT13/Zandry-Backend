from datetime import date, timedelta

from django.db.models import Count, Sum

from apps.appointments.models import Appointment
from apps.clients.models import Client
from apps.professionals.models import Professional
from apps.services.models import Service


def get_dashboard_summary(*, company, period_days=7):
    today = date.today()
    tomorrow = today + timedelta(days=1)
    period_days = max(1, min(int(period_days), 90))
    period_start = today - timedelta(days=period_days - 1)

    base_appointments = Appointment.objects.filter(company=company, active=True)

    status_counts = {
        row["status"]: row["total"] for row in base_appointments.values("status").annotate(total=Count("id"))
    }

    recent_daily_map = {
        row["date"]: row["total"]
        for row in base_appointments.filter(date__gte=period_start, date__lte=today)
        .values("date")
        .annotate(total=Count("id"))
    }
    recent_daily = [
        {
            "date": period_start + timedelta(days=idx),
            "total": recent_daily_map.get(period_start + timedelta(days=idx), 0),
        }
        for idx in range(period_days)
    ]

    return {
        "period_days": period_days,
        "totals": {
            "clients": Client.objects.filter(company=company, active=True).count(),
            "professionals": Professional.objects.filter(company=company, active=True).count(),
            "services": Service.objects.filter(company=company, active=True).count(),
            "appointments": base_appointments.count(),
        },
        "appointments": {
            "today": base_appointments.filter(date=today).count(),
            "tomorrow": base_appointments.filter(date=tomorrow).count(),
            "pending": status_counts.get("pending", 0),
            "confirmed": status_counts.get("confirmed", 0),
            "completed": status_counts.get("completed", 0),
            "cancelled": status_counts.get("cancelled", 0),
        },
        "revenue": {
            "completed_count": status_counts.get("completed", 0),
            "completed_amount": (
                base_appointments.filter(status="completed").aggregate(total=Sum("service__price"))["total"] or 0
            ),
        },
        "recent_daily": recent_daily,
    }
