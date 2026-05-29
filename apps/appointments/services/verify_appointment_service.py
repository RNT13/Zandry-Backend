from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.appointments.models.appointment_model import Appointment
from apps.appointments.models.appointment_verification_model import AppointmentVerification


@transaction.atomic
def verify_appointment_by_token(*, token: str) -> Appointment:
    token_hash = AppointmentVerification.hash_token(token)

    try:
        verification = AppointmentVerification.objects.select_related("appointment").get(token_hash=token_hash)
    except AppointmentVerification.DoesNotExist:
        raise ValidationError({"token": "Token inválido."})

    if verification.is_verified:
        return verification.appointment

    if verification.is_expired:
        raise ValidationError({"token": "Token expirado."})

    appointment = verification.appointment
    appointment.status = "confirmed"
    appointment.save(update_fields=["status", "updated_at"])

    verification.verified_at = timezone.now()
    verification.save(update_fields=["verified_at", "updated_at"])

    return appointment
