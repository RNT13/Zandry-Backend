from django.db import models

from common.models import BaseModel


class SubscriptionPlan(BaseModel):
    PLAN_CHOICES = (
        ("trial", "Trial"),
        ("start", "Start"),
        ("pro", "Pro"),
        ("business", "Business"),
    )

    code = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=100, blank=True, null=True)
    subtitle = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    recommended = models.BooleanField(default=False)
    coming_soon = models.BooleanField(default=False)

    monthly_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    max_professionals = models.IntegerField(default=1)
    max_services = models.IntegerField(default=3)
    max_appointments = models.IntegerField(default=30)

    allow_chat = models.BooleanField(default=False)
    allow_reports = models.BooleanField(default=False)
    allow_automation = models.BooleanField(default=False)
    allow_full_dashboard = models.BooleanField(default=False)

    trial_days = models.IntegerField(default=0)
    features = models.JSONField(default=list, blank=True)

    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "subscription_plans"
        ordering = ["sort_order"]

    def __str__(self):
        return self.name
