from django.utils import timezone

from apps.notifications.models.notification_delivery_model import NotificationDelivery


def mark_delivery_as_read(delivery: NotificationDelivery) -> NotificationDelivery:
    if delivery.status != "read":
        delivery.status = "read"
        delivery.read_at = timezone.now()
        delivery.save(update_fields=["status", "read_at"])
    return delivery
