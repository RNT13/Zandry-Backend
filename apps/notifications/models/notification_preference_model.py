from django.db import models

from common.models import BaseTenantModel


class NotificationPreference(BaseTenantModel):
    class RecipientTypeChoices(models.TextChoices):
        OWNER = "owner", "Owner"
        PROFESSIONAL = "professional", "Professional"
        CLIENT = "client", "Client"
        STAFF = "staff", "Staff"

    recipient_type = models.CharField(max_length=20, choices=RecipientTypeChoices.choices)

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notification_preferences",
    )

    professional = models.ForeignKey(
        "professionals.Professional",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notification_preferences",
    )

    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notification_preferences",
    )

    allow_in_app = models.BooleanField(default=True)
    allow_whatsapp = models.BooleanField(default=True)
    allow_email = models.BooleanField(default=True)

    booking_created = models.BooleanField(default=True)
    booking_confirmed = models.BooleanField(default=True)
    booking_cancelled = models.BooleanField(default=True)
    booking_reminder = models.BooleanField(default=True)
    subscription_expiring = models.BooleanField(default=True)
    system_message = models.BooleanField(default=True)

    class Meta:
        db_table = "notification_preferences"

    def __str__(self):
        return f"{self.company.name} - {self.recipient_type}"
