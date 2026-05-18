from datetime import date, timedelta

from django.db.models import Count, Sum

from apps.appointments.models import Appointment
from apps.clients.models import Client
from apps.professionals.models import Professional
from apps.services.models import Service


def get_dashboard_summary(*, company):
    today = date.today()
    tomorrow = today + timedelta(days=1)

    base_appointments = Appointment.objects.filter(company=company, active=True)

    status_counts = {
        row["status"]: row["total"] for row in base_appointments.values("status").annotate(total=Count("id"))
    }

    today_appointments = base_appointments.filter(date=today)

    return {
        "totals": {
            "clients": Client.objects.filter(company=company, active=True).count(),
            "professionals": Professional.objects.filter(company=company, active=True).count(),
            "services": Service.objects.filter(company=company, active=True).count(),
            "appointments": base_appointments.count(),
        },
        "appointments": {
            "today": today_appointments.count(),
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
    }
