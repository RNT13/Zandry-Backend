from __future__ import annotations

from datetime import datetime

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.appointments.models import Appointment
from apps.appointments.services.public_availability_service import validate_public_booking_slot
from apps.appointments.services.send_appointment_verification_email_service import send_appointment_verification_email
from apps.clients.services.upsert_client_service import upsert_public_client
from apps.companies.models import Company
from apps.notifications.services.booking_notifications_service import notify_booking_created
from apps.professionals.models import Professional
from apps.services.models import Service


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

    booking_date = validated_data["date"]
    booking_time = validated_data["time"]

    booking_dt = timezone.make_aware(
        datetime.combine(booking_date, booking_time),
        timezone.get_current_timezone(),
    )

    if booking_dt <= timezone.now():
        raise ValidationError({"time": "Esse horário já passou."})

    validate_public_booking_slot(
        company=company,
        service=service,
        professional=professional,
        booking_date=booking_date,
        booking_time=booking_time,
    )

    client = upsert_public_client(
        company,
        {
            "full_name": validated_data["user_name"],
            "phone": validated_data["user_phone"],
            "email": validated_data.get("user_email", ""),
        },
    )

    appointment = Appointment.objects.create(
        company=company,
        client=client,
        service=service,
        professional=professional,
        date=booking_date,
        time=booking_time,
        user_name=validated_data["user_name"],
        user_phone=validated_data["user_phone"],
        user_email=validated_data.get("user_email", ""),
        status="pending",
    )

    notify_booking_created(
        appointment=appointment,
        client=client,
    )

    send_appointment_verification_email(appointment=appointment)

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
