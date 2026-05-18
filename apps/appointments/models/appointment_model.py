from django.db import models

from common.models import BaseTenantModel


class Appointment(BaseTenantModel):
    STATUS_CHOICES = (
        ("pending", "Pendente"),
        ("confirmed", "Confirmado"),
        ("cancelled", "Cancelado"),
        ("completed", "Concluído"),
    )

    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments",
    )

    service = models.ForeignKey("services.Service", on_delete=models.CASCADE, related_name="appointments")
    professional = models.ForeignKey(
        "professionals.Professional", on_delete=models.CASCADE, related_name="appointments"
    )

    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    user_name = models.CharField(max_length=255)
    user_phone = models.CharField(max_length=20)
    user_email = models.EmailField(blank=True)

    class Meta:
        db_table = "appointments"
        unique_together = ("professional", "date", "time")
        ordering = ["date", "time"]

    def __str__(self):
        return f"{self.user_name} — {self.date} {self.time}"
