from rest_framework import serializers

from apps.professionals.serializers.public_response_serializer import PublicProfessionalBriefSerializer
from apps.services.models import Service


class PublicServiceSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(source="id", read_only=True)
    professionals = PublicProfessionalBriefSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = [
            "uid",
            "name",
            "description",
            "price",
            "duration",
            "professionals",
        ]
