from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone

from apps.notifications.models.notification_delivery_model import NotificationDelivery
from apps.notifications.models.notification_model import Notification


def send_email_notification(
    *,
    notification: Notification,
    delivery: NotificationDelivery,
    to_email: str,
    subject: str | None = None,
    text_body: str | None = None,
    html_body: str | None = None,
) -> NotificationDelivery:
    if not to_email:
        delivery.status = NotificationDelivery.StatusChoices.FAILED
        delivery.error_message = "Destinatário sem e-mail."
        delivery.save(update_fields=["status", "error_message", "updated_at"])
        return delivery

    message = EmailMultiAlternatives(
        subject=subject or notification.title or "Notificação Zandry",
        body=text_body or notification.body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )

    if html_body:
        message.attach_alternative(html_body, "text/html")

    try:
        sent_count = message.send(fail_silently=False)
    except Exception as exc:
        delivery.status = NotificationDelivery.StatusChoices.FAILED
        delivery.error_message = str(exc)
        delivery.save(update_fields=["status", "error_message", "updated_at"])

        notification.status = Notification.StatusChoices.FAILED
        notification.save(update_fields=["status", "updated_at"])

        return delivery

    if sent_count:
        delivery.status = NotificationDelivery.StatusChoices.SENT
        delivery.delivered_at = timezone.now()
        delivery.save(update_fields=["status", "delivered_at", "updated_at"])

        notification.status = Notification.StatusChoices.SENT
        notification.sent_at = timezone.now()
        notification.save(update_fields=["status", "sent_at", "updated_at"])
    else:
        delivery.status = NotificationDelivery.StatusChoices.FAILED
        delivery.error_message = "Nenhum e-mail foi enviado pelo backend de e-mail."
        delivery.save(update_fields=["status", "error_message", "updated_at"])

    return delivery
