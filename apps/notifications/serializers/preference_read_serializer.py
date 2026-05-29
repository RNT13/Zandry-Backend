from rest_framework import serializers

from apps.notifications.models.notification_preference_model import NotificationPreference


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(source="id", read_only=True)

    class Meta:
        model = NotificationPreference
        fields = [
            "uid",
            "recipient_type",
            "allow_in_app",
            "allow_whatsapp",
            "allow_email",
            "booking_created",
            "booking_confirmed",
            "booking_cancelled",
            "booking_reminder",
            "subscription_expiring",
            "system_message",
        ]
