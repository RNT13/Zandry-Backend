from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema

from apps.clients.models import Client
from apps.clients.serializers.public_response_serializer import PublicClientResponseSerializer


class ClientListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PublicClientResponseSerializer

    @extend_schema(responses={200: PublicClientResponseSerializer(many=True)})
    def get_queryset(self):
        return Client.objects.filter(company=self.request.user.company, active=True).order_by("full_name")
