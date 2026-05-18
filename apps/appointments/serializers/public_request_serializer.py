from rest_framework import serializers


class PublicAvailabilityQuerySerializer(serializers.Serializer):
    service_uid = serializers.UUIDField(required=True)
    professional_uid = serializers.UUIDField(required=True)
    date = serializers.DateField(required=False)


class PublicCreateBookingSerializer(serializers.Serializer):
    company_slug = serializers.SlugField()
    service_uid = serializers.UUIDField()
    professional_uid = serializers.UUIDField()
    date = serializers.DateField()
    time = serializers.TimeField()
    user_name = serializers.CharField(max_length=255)
    user_phone = serializers.CharField(max_length=20)
    user_email = serializers.EmailField(required=False, allow_blank=True)
