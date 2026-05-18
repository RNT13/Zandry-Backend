from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema

from apps.notifications.models.notification_delivery_model import NotificationDelivery
from apps.notifications.serializers.notification_read_serializer import NotificationDeliveryReadSerializer
from apps.notifications.serializers.notification_write_serializer import NotificationMarkAsReadSerializer
from apps.notifications.services.mark_as_read_service import mark_delivery_as_read
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView


class MyNotificationListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationDeliveryReadSerializer

    @extend_schema(responses={200: NotificationDeliveryReadSerializer(many=True)})
    def get_queryset(self):
        user = self.request.user
        return (
            NotificationDelivery.objects
            .select_related("notification", "user")
            .filter(user=user)
            .order_by("-created_at")
        )


class MarkNotificationAsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=NotificationMarkAsReadSerializer)
    def post(self, request):
        serializer = NotificationMarkAsReadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        delivery = get_object_or_404(
            NotificationDelivery,
            id=serializer.validated_data["delivery_id"],
            user=request.user,
        )

        delivery = mark_delivery_as_read(delivery)

        return Response(
            {
                "success": True,
                "message": "Notificação marcada como lida.",
                "delivery_id": str(delivery.id),
            }
        )
