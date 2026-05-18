from rest_framework import serializers
from apps.companies.models import Company, BusinessHour


class BusinessHourReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessHour
        fields = ["week_day", "start", "end", "is_open"]


class CompanyReadSerializer(serializers.ModelSerializer):
    business_hours = BusinessHourReadSerializer(many=True, read_only=True)
    logo = serializers.CharField(read_only=True, allow_null=True)
    banner = serializers.CharField(read_only=True, allow_null=True)

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "slug",
            "rating",
            "cnpj",
            "email",
            "phone",
            "category",
            "description",
            "logo",
            "banner",
            "cep",
            "address",
            "number",
            "city",
            "state",
            "advantage1",
            "advantage2",
            "advantage3",
            "business_hours",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request")

        data["logo"] = request.build_absolute_uri(instance.logo.url) if instance.logo and request else None
        data["banner"] = request.build_absolute_uri(instance.banner.url) if instance.banner and request else None
        return data
