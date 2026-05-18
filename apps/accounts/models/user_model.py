from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from common.models import BaseModel
from rest_framework.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValidationError("O usuário deve possuir email")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            full_name=full_name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, full_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    ROLE_CHOICES = (
        ("owner", "Owner"),
        ("manager", "Manager"),
        ("staff", "Staff"),
    )

    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True
    )

    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="owner")

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email
