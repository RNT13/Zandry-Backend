from rest_framework import serializers

from apps.notifications.models.notification_delivery_model import NotificationDelivery
from apps.notifications.models.notification_model import Notification


class NotificationReadSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(source="id", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "uid",
            "event_key",
            "channel",
            "title",
            "body",
            "payload",
            "status",
            "scheduled_for",
            "sent_at",
            "created_at",
        ]


class NotificationSummarySerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(source="id", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "uid",
            "event_key",
            "channel",
            "title",
            "body",
            "payload",
            "status",
            "created_at",
            "sent_at",
        ]


class NotificationDeliveryReadSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(source="id", read_only=True)
    notification = NotificationSummarySerializer(read_only=True)

    class Meta:
        model = NotificationDelivery
        fields = [
            "uid",
            "recipient_type",
            "status",
            "read_at",
            "delivered_at",
            "provider_message_id",
            "error_message",
            "notification",
            "created_at",
        ]
