from django.db import models
from common.models import BaseModel


class Company(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0)

    cnpj = models.CharField(max_length=18, unique=True)

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)

    category = models.CharField(max_length=100)
    description = models.TextField()

    logo = models.ImageField(upload_to="companies/logos/", blank=True, null=True)
    banner = models.ImageField(upload_to="companies/banners/", blank=True, null=True)

    cep = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    advantage1 = models.CharField(max_length=255, blank=True)
    advantage2 = models.CharField(max_length=255, blank=True)
    advantage3 = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "companies"

    def __str__(self):
        return self.name
