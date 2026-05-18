from django.db import models
from common.models import BaseTenantModel


class Notification(BaseTenantModel):
    class ChannelChoices(models.TextChoices):
        IN_APP = "in_app", "In App"
        WHATSAPP = "whatsapp", "WhatsApp"

    class EventChoices(models.TextChoices):
        BOOKING_CREATED = "booking_created", "Booking Created"
        BOOKING_CONFIRMED = "booking_confirmed", "Booking Confirmed"
        BOOKING_CANCELLED = "booking_cancelled", "Booking Cancelled"
        BOOKING_REMINDER = "booking_reminder", "Booking Reminder"
        SUBSCRIPTION_EXPIRING = "subscription_expiring", "Subscription Expiring"
        SYSTEM_MESSAGE = "system_message", "System Message"

    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        QUEUED = "queued", "Queued"
        SENT = "sent", "Sent"
        DELIVERED = "delivered", "Delivered"
        FAILED = "failed", "Failed"

    event_key = models.CharField(max_length=50, choices=EventChoices.choices)
    channel = models.CharField(max_length=20, choices=ChannelChoices.choices)

    title = models.CharField(max_length=255, blank=True)
    body = models.TextField()

    payload = models.JSONField(default=dict, blank=True)

    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.event_key} - {self.channel}"
