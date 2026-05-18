from rest_framework import serializers


class NotificationMarkAsReadSerializer(serializers.Serializer):
    delivery_id = serializers.UUIDField()
