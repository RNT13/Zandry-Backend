from django.db import models

from common.models import BaseTenantModel


class Client(BaseTenantModel):
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)

    whatsapp_verified = models.BooleanField(default=False)
    whatsapp_verified_at = models.DateTimeField(blank=True, null=True)

    notes = models.TextField(blank=True, default="")

    class Meta:
        db_table = "clients"
        ordering = ["full_name"]
        constraints = [models.UniqueConstraint(fields=["company", "phone"], name="unique_client_phone_per_company")]

    def __str__(self):
        return f"{self.full_name} - {self.phone}"
