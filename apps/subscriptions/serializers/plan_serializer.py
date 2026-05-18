# apps/subscriptions/serializers.py

from rest_framework import serializers
from apps.subscriptions.models.plan_model import SubscriptionPlan


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    limits = serializers.SerializerMethodField()

    class Meta:
        model = SubscriptionPlan
        fields = [
            "id", "code", "name", "title", "subtitle", "description",
            "recommended", "coming_soon",
            "monthly_price", "price",
            "trial_days", "features", "limits",
            "sort_order",
        ]

    def get_price(self, obj):
        value = float(obj.monthly_price)
        if value == 0:
            return "Grátis"
        return f"R${value:,.2f}/mês".replace(",", "X").replace(".", ",").replace("X", ".")

    def get_limits(self, obj):
        return {
            "max_professionals":  obj.max_professionals,
            "max_services":       obj.max_services,
            "max_appointments":   obj.max_appointments,
            "allow_chat":         obj.allow_chat,
            "allow_reports":      obj.allow_reports,
            "allow_automation":   obj.allow_automation,
            "allow_full_dashboard": obj.allow_full_dashboard,
        }
