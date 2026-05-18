from rest_framework import serializers

from apps.subscriptions.models.usage_model import SubscriptionUsage


class SubscriptionUsageReadSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(source="id", read_only=True)
    company_slug = serializers.CharField(source="company.slug", read_only=True)
    company_name = serializers.CharField(source="company.name", read_only=True)
    plan_code = serializers.CharField(source="plan.code", read_only=True)
    plan_name = serializers.CharField(source="plan.name", read_only=True)

    class Meta:
        model = SubscriptionUsage
        fields = [
            "uid",
            "company_slug",
            "company_name",
            "plan_code",
            "plan_name",
            "status",
            "expires_at",
            "current_professionals",
            "current_services",
            "current_appointments",
        ]
