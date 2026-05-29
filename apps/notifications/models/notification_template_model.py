from django.db import models

from common.models import BaseModel


class NotificationTemplate(BaseModel):
    class ChannelChoices(models.TextChoices):
        IN_APP = "in_app", "In App"
        WHATSAPP = "whatsapp", "WhatsApp"
        EMAIL = "email", "Email"

    class EventChoices(models.TextChoices):
        BOOKING_CREATED = "booking_created", "Booking Created"
        BOOKING_CONFIRMED = "booking_confirmed", "Booking Confirmed"
        BOOKING_CANCELLED = "booking_cancelled", "Booking Cancelled"
        BOOKING_REMINDER = "booking_reminder", "Booking Reminder"
        SUBSCRIPTION_EXPIRING = "subscription_expiring", "Subscription Expiring"
        SYSTEM_MESSAGE = "system_message", "System Message"

    class AudienceChoices(models.TextChoices):
        OWNER = "owner", "Owner"
        PROFESSIONAL = "professional", "Professional"
        CLIENT = "client", "Client"
        STAFF = "staff", "Staff"

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="notification_templates",
        null=True,
        blank=True,
    )

    event_key = models.CharField(max_length=50, choices=EventChoices.choices)
    channel = models.CharField(max_length=20, choices=ChannelChoices.choices)
    audience = models.CharField(max_length=20, choices=AudienceChoices.choices)

    title_template = models.CharField(max_length=255, blank=True)
    body_template = models.TextField()

    placeholders = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "notification_templates"
        ordering = ["event_key", "channel", "audience"]

    def __str__(self):
        return f"{self.event_key} - {self.channel} - {self.audience}"
