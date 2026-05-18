from rest_framework import serializers


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(required=False, default=False)


class AuthOwnerRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)


class AuthCompanyRegisterSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=255)
    cnpj = serializers.CharField(max_length=18)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    category = serializers.CharField(max_length=100)
    description = serializers.CharField()


class AuthAddressRegisterSerializer(serializers.Serializer):
    cep = serializers.CharField(max_length=10)
    address = serializers.CharField(max_length=255)
    number = serializers.CharField(max_length=20)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=100)


class AuthBusinessHourRegisterSerializer(serializers.Serializer):
    week_day = serializers.ChoiceField(
        choices=[
            ("monday", "Monday"),
            ("tuesday", "Tuesday"),
            ("wednesday", "Wednesday"),
            ("thursday", "Thursday"),
            ("friday", "Friday"),
            ("saturday", "Saturday"),
            ("sunday", "Sunday"),
        ]
    )
    start = serializers.CharField(max_length=5, required=False, allow_blank=True)
    end = serializers.CharField(max_length=5, required=False, allow_blank=True)
    is_open = serializers.BooleanField(required=False, default=False)


class AuthAdvantagesRegisterSerializer(serializers.Serializer):
    advantage1 = serializers.CharField(required=False, allow_blank=True, default="")
    advantage2 = serializers.CharField(required=False, allow_blank=True, default="")
    advantage3 = serializers.CharField(required=False, allow_blank=True, default="")


class AuthServiceRegisterSerializer(serializers.Serializer):
    uid = serializers.CharField(required=False)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True, default="")
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    duration = serializers.IntegerField()


class AuthProfessionalRegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    position = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    services_ids = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=list,
    )


class AuthSubscriptionRegisterSerializer(serializers.Serializer):
    selected_plan = serializers.CharField()
