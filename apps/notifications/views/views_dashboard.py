from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema

from apps.notifications.models.notification_preference_model import NotificationPreference
from apps.notifications.serializers.preference_read_serializer import NotificationPreferenceSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView


class MyNotificationPreferenceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: NotificationPreferenceSerializer})
    def get(self, request):
        pref = NotificationPreference.objects.filter(
            company=request.user.company,
            user=request.user,
        ).first()

        if not pref:
            pref = NotificationPreference.objects.create(
                company=request.user.company,
                user=request.user,
                recipient_type="owner",
            )

        return Response(NotificationPreferenceSerializer(pref).data)

    @extend_schema(request=NotificationPreferenceSerializer, responses={200: NotificationPreferenceSerializer})
    def patch(self, request):
        pref = NotificationPreference.objects.filter(
            company=request.user.company,
            user=request.user,
        ).first()

        if not pref:
            pref = NotificationPreference.objects.create(
                company=request.user.company,
                user=request.user,
                recipient_type="owner",
            )

        serializer = NotificationPreferenceSerializer(pref, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
