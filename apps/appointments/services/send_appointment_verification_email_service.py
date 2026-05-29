from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from apps.appointments.models.appointment_verification_model import AppointmentVerification
from apps.notifications.models.notification_model import Notification
from apps.notifications.services.create_notification_service import create_delivery, create_notification
from apps.notifications.services.send_email_notification_service import send_email_notification


def send_appointment_verification_email(*, appointment) -> AppointmentVerification | None:
    if not appointment.user_email:
        return None

    token = AppointmentVerification.generate_token()
    token_hash = AppointmentVerification.hash_token(token)

    verification, _ = AppointmentVerification.objects.update_or_create(
        appointment=appointment,
        defaults={
            "token_hash": token_hash,
            "expires_at": timezone.now() + timedelta(hours=24),
            "verified_at": None,
        },
    )

    verify_url = f"{settings.FRONTEND_URL}/agendamento/verificar?token={token}"

    notification = create_notification(
        company=appointment.company,
        event_key=Notification.EventChoices.BOOKING_CREATED,
        channel=Notification.ChannelChoices.EMAIL,
        title="Confirme seu agendamento",
        body=(
            f"Olá {appointment.user_name}, confirme seu agendamento em "
            f"{appointment.date} às {appointment.time.strftime('%H:%M')}."
        ),
        payload={
            "appointment_id": str(appointment.id),
            "verification_id": str(verification.id),
            "verify_url": verify_url,
        },
    )

    delivery = create_delivery(
        notification=notification,
        recipient_type="client",
        client=appointment.client,
    )

    html_body = f"""
    <p>Olá, {appointment.user_name}!</p>
    <p>Seu agendamento foi criado e está aguardando confirmação.</p>
    <p><strong>Data:</strong> {appointment.date}</p>
    <p><strong>Horário:</strong> {appointment.time.strftime("%H:%M")}</p>
    <p><strong>Serviço:</strong> {appointment.service.name}</p>
    <p><strong>Profissional:</strong> {appointment.professional.full_name}</p>
    <p>
        <a href="{verify_url}">Clique aqui para confirmar seu agendamento</a>
    </p>
    <p>Esse link expira em 24 horas.</p>
    """

    send_email_notification(
        notification=notification,
        delivery=delivery,
        to_email=appointment.user_email,
        subject="Confirme seu agendamento na Zandry",
        text_body=notification.body + f"\n\nConfirme aqui: {verify_url}",
        html_body=html_body,
    )

    return verification
