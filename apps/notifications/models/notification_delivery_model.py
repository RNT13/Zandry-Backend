from django.db import models

from common.models import BaseModel


class NotificationDelivery(BaseModel):
    class RecipientTypeChoices(models.TextChoices):
        OWNER = "owner", "Owner"
        PROFESSIONAL = "professional", "Professional"
        CLIENT = "client", "Client"
        STAFF = "staff", "Staff"

    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        SENT = "sent", "Sent"
        DELIVERED = "delivered", "Delivered"
        READ = "read", "Read"
        FAILED = "failed", "Failed"

    notification = models.ForeignKey(
        "notifications.Notification",
        on_delete=models.CASCADE,
        related_name="deliveries",
    )

    recipient_type = models.CharField(max_length=20, choices=RecipientTypeChoices.choices)

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notification_deliveries",
    )

    professional = models.ForeignKey(
        "professionals.Professional",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notification_deliveries",
    )

    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notification_deliveries",
    )

    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    read_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    provider_message_id = models.CharField(max_length=255, blank=True)
    error_message = models.TextField(blank=True)

    class Meta:
        db_table = "notification_deliveries"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.notification_id} - {self.recipient_type}"
