from rest_framework import serializers

from apps.subscriptions.models.plan_model import SubscriptionPlan


class SubscriptionPlanLimitsSerializer(serializers.Serializer):
    max_professionals = serializers.IntegerField()
    max_services = serializers.IntegerField()
    max_appointments = serializers.IntegerField()
    allow_chat = serializers.BooleanField()
    allow_reports = serializers.BooleanField()
    allow_automation = serializers.BooleanField()
    allow_full_dashboard = serializers.BooleanField()


class SubscriptionPlanReadSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(source="id", read_only=True)
    price = serializers.CharField(read_only=True)
    limits = SubscriptionPlanLimitsSerializer(read_only=True)

    class Meta:
        model = SubscriptionPlan
        fields = [
            "uid",
            "code",
            "name",
            "title",
            "subtitle",
            "description",
            "recommended",
            "coming_soon",
            "monthly_price",
            "price",
            "trial_days",
            "features",
            "limits",
            "sort_order",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        monthly = float(instance.monthly_price)

        if monthly == 0:
            data["price"] = "Grátis"
        else:
            data["price"] = f"R${monthly:,.2f}/mês".replace(",", "X").replace(".", ",").replace("X", ".")

        data["limits"] = {
            "max_professionals": instance.max_professionals,
            "max_services": instance.max_services,
            "max_appointments": instance.max_appointments,
            "allow_chat": instance.allow_chat,
            "allow_reports": instance.allow_reports,
            "allow_automation": instance.allow_automation,
            "allow_full_dashboard": instance.allow_full_dashboard,
        }

        return data
