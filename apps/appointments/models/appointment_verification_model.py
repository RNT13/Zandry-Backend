import hashlib
import secrets

from django.db import models
from django.utils import timezone

from common.models import BaseModel


class AppointmentVerification(BaseModel):
    appointment = models.OneToOneField(
        "appointments.Appointment",
        on_delete=models.CASCADE,
        related_name="verification",
    )

    token_hash = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "appointment_verifications"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Verification for appointment {self.appointment_id}"

    @staticmethod
    def generate_token() -> str:
        return secrets.token_urlsafe(32)

    @staticmethod
    def hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    @property
    def is_expired(self) -> bool:
        return timezone.now() > self.expires_at

    @property
    def is_verified(self) -> bool:
        return self.verified_at is not None
