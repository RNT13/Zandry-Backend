from rest_framework import serializers

from apps.companies.models import Company


class CompanyWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
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
        ]
