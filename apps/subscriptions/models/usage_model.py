from django.db import models
from common.models import BaseModel


class SubscriptionUsage(BaseModel):
    STATUS_CHOICES = (
        ("trial", "Trial"),
        ("active", "Active"),
        ("expired", "Expired"),
        ("cancelled", "Cancelled"),
    )

    company = models.OneToOneField(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="subscription_usage"
    )

    plan = models.ForeignKey(
        "subscriptions.SubscriptionPlan",
        on_delete=models.PROTECT,
        related_name="companies_usage"
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="trial")

    expires_at = models.DateTimeField()

    current_professionals = models.IntegerField(default=0)
    current_services = models.IntegerField(default=0)
    current_appointments = models.IntegerField(default=0)

    class Meta:
        db_table = "subscription_usage"

    def __str__(self):
        return f"{self.company.name} - {self.plan.name}"
