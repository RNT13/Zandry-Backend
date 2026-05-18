from rest_framework import serializers
from apps.clients.models import Client


class PublicClientResponseSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(source="id", read_only=True)

    class Meta:
        model = Client
        fields = [
            "uid",
            "full_name",
            "phone",
            "email",
            "whatsapp_verified",
            "whatsapp_verified_at",
            "notes",
        ]
