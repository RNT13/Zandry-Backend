from rest_framework import serializers

from apps.notifications.models.notification_template_model import NotificationTemplate


class NotificationTemplateReadSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(source="id", read_only=True)

    class Meta:
        model = NotificationTemplate
        fields = [
            "uid",
            "company",
            "event_key",
            "channel",
            "audience",
            "title_template",
            "body_template",
            "placeholders",
            "is_active",
        ]
