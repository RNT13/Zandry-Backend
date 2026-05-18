from apps.notifications.services.create_notification_service import create_notification, create_delivery


def notify_booking_created(*, appointment, client=None):
    company = appointment.company

    notification = create_notification(
        company=company,
        event_key="booking_created",
        channel="in_app",
        title="Novo agendamento",
        body=f"Novo agendamento para {appointment.user_name} em {appointment.date} às {appointment.time.strftime('%H:%M')}.",
        payload={
            "appointment_id": str(appointment.id),
            "service_id": str(appointment.service_id),
            "professional_id": str(appointment.professional_id),
            "client_id": str(client.id) if client else None,
        },
    )

    owners = company.users.filter(role="owner", active=True)
    for owner in owners:
        create_delivery(
            notification=notification,
            recipient_type="owner",
            user=owner,
        )

    create_delivery(
        notification=notification,
        recipient_type="professional",
        professional=appointment.professional,
    )

    if client:
        create_delivery(
            notification=notification,
            recipient_type="client",
            client=client,
        )

    return notification
