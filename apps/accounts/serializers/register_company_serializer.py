from rest_framework import serializers

from .auth_request_serializer import (
    AuthOwnerRegisterSerializer,
    AuthCompanyRegisterSerializer,
    AuthAddressRegisterSerializer,
    AuthBusinessHourRegisterSerializer,
    AuthAdvantagesRegisterSerializer,
    AuthServiceRegisterSerializer,
    AuthProfessionalRegisterSerializer,
    AuthSubscriptionRegisterSerializer,
)


class RegisterCompanySerializer(serializers.Serializer):
    owner = AuthOwnerRegisterSerializer()
    company = AuthCompanyRegisterSerializer()
    address = AuthAddressRegisterSerializer()
    business_hours = AuthBusinessHourRegisterSerializer(many=True, required=False, default=list)
    advantages = AuthAdvantagesRegisterSerializer()
    services = AuthServiceRegisterSerializer(many=True, required=False, default=list)
    professionals = AuthProfessionalRegisterSerializer(many=True, required=False, default=list)
    subscription = AuthSubscriptionRegisterSerializer()

    def validate(self, attrs):
        owner = attrs.get("owner", {})
        password = owner.get("password")
        confirm_password = owner.get("confirm_password")

        if confirm_password is not None and password != confirm_password:
            raise serializers.ValidationError({
                "owner": {
                    "confirm_password": "As senhas não coincidem."
                }
            })

        return attrs
