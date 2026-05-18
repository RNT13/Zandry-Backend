from rest_framework import serializers


class PublicClientUpsertSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=20)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
