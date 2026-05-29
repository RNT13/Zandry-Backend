from rest_framework import serializers


class AuthUserResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    email = serializers.EmailField()
    full_name = serializers.CharField()
    role = serializers.CharField()
    company_slug = serializers.CharField(allow_null=True, required=False)


class LoginResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    access = serializers.CharField()
    user = AuthUserResponseSerializer()


class MeResponseSerializer(serializers.Serializer):
    id = serializers.CharField()
    email = serializers.EmailField()
    full_name = serializers.CharField()
    role = serializers.CharField()
    company_slug = serializers.CharField(allow_null=True, required=False)


class RefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()


class RegisterCompanyResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField()
    user = AuthUserResponseSerializer()
    company_id = serializers.CharField()
    company_slug = serializers.CharField()
    access = serializers.CharField()
