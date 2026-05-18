from django.db import models
from common.models import BaseTenantModel


class Service(BaseTenantModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Duração em minutos")

    class Meta:
        db_table = "services"
        ordering = ["name"]

    def __str__(self):
        return self.name
