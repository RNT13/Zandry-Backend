from rest_framework import serializers


class PublicSlotResponseSerializer(serializers.Serializer):
    date = serializers.DateField()
    time = serializers.CharField()
    available = serializers.BooleanField()


class PublicDayAvailabilityResponseSerializer(serializers.Serializer):
    date = serializers.DateField()
    label = serializers.CharField()
    weekday = serializers.CharField()
    is_open = serializers.BooleanField()
    slots = PublicSlotResponseSerializer(many=True)


class PublicBookingClientSerializer(serializers.Serializer):
    uid = serializers.UUIDField()
    full_name = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.CharField(allow_blank=True, allow_null=True, required=False)


class PublicAvailabilityResponseSerializer(serializers.Serializer):
    days = PublicDayAvailabilityResponseSerializer(many=True)


class PublicBookingResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    date = serializers.DateField()
    time = serializers.CharField()
    status = serializers.CharField()

    company = serializers.CharField()
    company_zip_code = serializers.CharField()
    company_address = serializers.CharField()
    company_number = serializers.CharField()

    service = serializers.CharField()
    service_duration = serializers.IntegerField()
    service_price = serializers.CharField()

    professional = serializers.CharField()

    client = PublicBookingClientSerializer()

    user_name = serializers.CharField()
    user_phone = serializers.CharField()
    user_email = serializers.CharField(allow_blank=True, required=False)
