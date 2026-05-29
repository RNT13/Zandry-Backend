from rest_framework import serializers


class AppointmentVerificationRequestSerializer(serializers.Serializer):
    token = serializers.CharField()
