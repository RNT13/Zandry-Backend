from django.db import transaction
from apps.notifications.models.notification_model import Notification
from apps.notifications.models.notification_delivery_model import NotificationDelivery


@transaction.atomic
def create_notification(
    *,
    company,
    event_key: str,
    channel: str,
    title: str,
    body: str,
    payload: dict | None = None,
    scheduled_for=None,
):
    notification = Notification.objects.create(
        company=company,
        event_key=event_key,
        channel=channel,
        title=title,
        body=body,
        payload=payload or {},
        scheduled_for=scheduled_for,
        status="pending",
    )
    return notification


@transaction.atomic
def create_delivery(
    *,
    notification,
    recipient_type: str,
    user=None,
    professional=None,
    client=None,
):
    return NotificationDelivery.objects.create(
        notification=notification,
        recipient_type=recipient_type,
        user=user,
        professional=professional,
        client=client,
        status="pending",
    )
