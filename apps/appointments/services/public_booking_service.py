from datetime import datetime, timedelta

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from apps.appointments.models import Appointment
from apps.appointments.services.public_availability_service import slots_needed
from apps.clients.services.upsert_client_service import upsert_public_client
from apps.companies.models import Company
from apps.notifications.services.booking_notifications_service import notify_booking_created
from apps.professionals.models import Professional
from apps.services.models import Service

SLOT_INTERVAL = 15


@transaction.atomic
def create_public_booking(validated_data: dict) -> dict:
    company = get_object_or_404(Company, slug=validated_data["company_slug"], active=True)
    service = get_object_or_404(Service, id=validated_data["service_uid"], company=company, active=True)
    professional = get_object_or_404(
        Professional,
        id=validated_data["professional_uid"],
        company=company,
        active=True,
        services=service,
    )

    client = upsert_public_client(
        company,
        {
            "full_name": validated_data["user_name"],
            "phone": validated_data["user_phone"],
            "email": validated_data.get("user_email", ""),
        },
    )

    n_slots = slots_needed(service.duration)
    start_time_str = validated_data["time"].strftime("%H:%M")

    occupied_times = []
    for offset in range(n_slots):
        dt = datetime.strptime(start_time_str, "%H:%M") + timedelta(minutes=offset * SLOT_INTERVAL)
        occupied_times.append(dt.strftime("%H:%M"))

    conflict = Appointment.objects.filter(
        professional=professional,
        date=validated_data["date"],
        time__in=[datetime.strptime(t, "%H:%M").time() for t in occupied_times],
        status__in=["pending", "confirmed"],
    ).exists()

    if conflict:
        raise ValidationError({"time": "Este horário já está reservado. Escolha outro."})

    appointment = Appointment.objects.create(
        company=company,
        client=client,
        service=service,
        professional=professional,
        date=validated_data["date"],
        time=validated_data["time"],
        user_name=validated_data["user_name"],
        user_phone=validated_data["user_phone"],
        user_email=validated_data.get("user_email", ""),
        status="pending",
    )

    for time_str in occupied_times[1:]:
        Appointment.objects.get_or_create(
            professional=professional,
            date=validated_data["date"],
            time=datetime.strptime(time_str, "%H:%M").time(),
            defaults={
                "company": company,
                "client": client,
                "service": service,
                "professional": professional,
                "user_name": f"[bloqueado] {validated_data['user_name']}",
                "user_phone": validated_data["user_phone"],
                "user_email": "",
                "status": "confirmed",
            },
        )

    notify_booking_created(
        appointment=appointment,
        client=client,
    )

    return {
        "id": str(appointment.id),
        "date": appointment.date,
        "time": appointment.time.strftime("%H:%M"),
        "status": appointment.status,
        "company": company.name,
        "company_zip_code": company.cep,
        "company_address": company.address,
        "company_number": company.number,
        "service": service.name,
        "service_duration": service.duration,
        "service_price": str(service.price),
        "professional": professional.full_name,
        "client": {
            "uid": str(client.id),
            "full_name": client.full_name,
            "phone": client.phone,
            "email": client.email,
        },
        "user_name": appointment.user_name,
        "user_phone": appointment.user_phone,
        "user_email": appointment.user_email,
    }
