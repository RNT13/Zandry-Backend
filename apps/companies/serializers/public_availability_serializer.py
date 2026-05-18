from rest_framework import serializers


class PublicSlotAvailabilitySerializer(serializers.Serializer):
    date = serializers.DateField()
    time = serializers.CharField()
    available = serializers.BooleanField()


class PublicDayAvailabilitySerializer(serializers.Serializer):
    date = serializers.DateField()
    label = serializers.CharField()
    weekday = serializers.CharField()
    is_open = serializers.BooleanField()
    slots = PublicSlotAvailabilitySerializer(many=True)


class PublicAvailabilitySerializer(serializers.Serializer):
    days = PublicDayAvailabilitySerializer(many=True)
