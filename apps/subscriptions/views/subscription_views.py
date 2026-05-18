from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema

from apps.subscriptions.models.plan_model import SubscriptionPlan
from apps.subscriptions.serializers.plan_response_serializer import SubscriptionPlanReadSerializer


class SubscriptionPlanListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SubscriptionPlanReadSerializer

    @extend_schema(responses={200: SubscriptionPlanReadSerializer(many=True)})
    def get_queryset(self):
        return SubscriptionPlan.objects.filter(is_active=True).order_by("sort_order")
