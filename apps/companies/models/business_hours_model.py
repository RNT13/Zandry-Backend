from django.db import models

from common.models import BaseTenantModel


class BusinessHour(BaseTenantModel):
    WEEKDAY_CHOICES = (
        ("monday", "Segunda-feira"),
        ("tuesday", "Terça-feira"),
        ("wednesday", "Quarta-feira"),
        ("thursday", "Quinta-feira"),
        ("friday", "Sexta-feira"),
        ("saturday", "Sábado"),
        ("sunday", "Domingo"),
    )

    week_day = models.CharField(max_length=20, choices=WEEKDAY_CHOICES)
    start = models.CharField(max_length=5, blank=True)  # "08:00"
    end = models.CharField(max_length=5, blank=True)  # "18:00"
    is_open = models.BooleanField(default=False)

    class Meta:
        db_table = "business_hours"
        unique_together = ("company", "week_day")
        ordering = ["week_day"]

    company = models.ForeignKey("companies.Company", on_delete=models.CASCADE, related_name="business_hours")
