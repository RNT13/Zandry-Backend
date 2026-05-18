from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.serializers.auth_response_serializer import MeResponseSerializer


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: MeResponseSerializer})
    def get(self, request):
        u = request.user
        return Response(
            {
                "id": str(u.id),
                "email": u.email,
                "full_name": u.full_name,
                "role": u.role,
                "company_slug": u.company.slug if u.company else None,
            }
        )
