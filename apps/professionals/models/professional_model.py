from django.db import models

from common.models import BaseTenantModel


class Professional(BaseTenantModel):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=150)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)

    avatar = models.ImageField(upload_to="professionals/avatars/", blank=True, null=True)

    phone = models.CharField(max_length=20, blank=True)

    services = models.ManyToManyField("services.Service", related_name="professionals", blank=True)

    class Meta:
        db_table = "professionals"
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name
